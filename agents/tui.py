"""Terminal UI for conversing with the software quality engineer."""

from __future__ import annotations

import asyncio
import sys
import threading
from collections.abc import Callable

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Input, RichLog

from agents.contracts import AgentRole
from agents.qa_engineer import QualityEngineerSession
from agents.tui_activity import build_ui_callbacks
from agents.tui_commands import SlashAction, parse_slash_command
from agents.tui_orchestrator import QATUIOrchestrator
from agents.tui_render import write_assistant_markdown
from agents.tui_theme import GREEN_THEME_CSS
from agents.tui_widgets import ActivityRail, IdleStatusRail, StreamPreview
from services.gemini_client import (
    GeminiChatClient,
    GeminiConfigurationError,
    GeminiRequestError,
)
from services.local_env import load_project_dotenv


def _format_provider_error(exc: GeminiRequestError) -> str:
    message = str(exc)
    if "HTTP 503" in message:
        return (
            "[bold red]Gemini provider error (HTTP 503)[/] — temporary Google overload, not Playwright MCP. "
            "Retry, set GEMINI_FALLBACK_MODEL=gemini-2.0-flash in .env, or run "
            "`python scripts/diagnose_mcp.py` to separate provider vs ShopDemo issues."
        )
    return f"[bold red]Provider error[/]: {exc}"


HELP_TEXT = """[bold #58ff58]Commands[/]
  /help              — show this help
  /clear             — new conversation
  /quit              — exit
  /agents            — list specialized agent roles
  /agent <role> <prompt> — run one agent (with file + MCP preflight tools)
  /flow <goal>         — same as typing a goal without / (multi-agent + files + MCP)
  /chat <question>     — advisor-only (no files, no MCP tools)

[bold #58ff58]Default[/]
  Plain text (no slash) runs the multi-agent QA flow and writes tests when possible.

[bold #58ff58]Agent roles[/]
  requirement-analyzer, test-planner, playwright-engineer,
  failure-analyzer, qa-reviewer

[bold #58ff58]Example[/]
  /agent requirement-analyzer Review ShopDemo checkout scope

[bold #58ff58]Tips[/]
  Lines starting with `/` are commands, not chat.
  Free-form text (no `/`) uses the QA engineer persona.
"""


class QAEngineerApp(App[None]):
    """Chat-style TUI for the quality engineer assistant."""

    TITLE = "Software Quality Engineer"
    SUB_TITLE = "Autonomous QA Engineer"
    CSS = GREEN_THEME_CSS

    BINDINGS = [
        Binding("ctrl+l", "clear_chat", "Clear", show=False),
        Binding("ctrl+q", "quit", "Quit", show=False),
    ]

    def __init__(self, orchestrator: QATUIOrchestrator) -> None:
        super().__init__()
        self.orchestrator = orchestrator
        self._busy = False
        self._flush_stream = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="chat", highlight=True, markup=True, wrap=True)
        yield StreamPreview(id="stream")
        yield ActivityRail(id="activity")
        yield IdleStatusRail(id="idle")
        yield Input(id="prompt", placeholder="Goal → multi-agent flow  (/chat for advice only)")
        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#chat", RichLog)
        log.write(
            "[bold #43ff43]QA flow[/] ready — type a goal to run analyzer → planner → playwright "
            "(files + Playwright MCP tools).\n"
            "[dim]Spinner, tool trail, and live stream show while work runs. "
            "Use [bold]/chat[/] for advice-only. [bold]/help[/] for commands.[/]"
        )
        self.query_one("#prompt", Input).focus()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.query_one("#prompt", Input).disabled = busy
        self.query_one("#idle", IdleStatusRail).set_busy(busy)

    def _activity(self) -> ActivityRail:
        return self.query_one("#activity", ActivityRail)

    def _stream(self) -> StreamPreview:
        return self.query_one("#stream", StreamPreview)

    def _post_to_ui(self, update: Callable[[], None]) -> None:
        """Schedule UI work from worker thread, or run immediately on UI thread."""

        if threading.get_ident() == self._thread_id:
            update()
        else:
            self.call_from_thread(update)

    def _begin_work(self, activity_message: str, stream_heading: str) -> tuple:
        activity = self._activity()
        stream = self._stream()
        activity.start(activity_message)
        stream.show_stream(stream_heading, "…")
        on_phase, on_stream, flush_stream = build_ui_callbacks(
            activity,
            stream,
            stream_heading=stream_heading,
            post_to_ui=self._post_to_ui,
        )
        self._flush_stream = flush_stream
        return on_phase, on_stream

    def _end_work(self) -> None:
        flush = getattr(self, "_flush_stream", None)
        if flush is not None:
            flush()
        self._stream().hide_stream()
        self._activity().stop()
        self._flush_stream = None

    def _write_agent_catalog(self, log: RichLog) -> None:
        lines = ["[bold #58ff58]Specialized agents[/]", ""]
        for role in AgentRole:
            spec = self.orchestrator.registry.get(role).spec
            lines.append(f"[bold #7dffb8]{role.value}[/] — {spec.description}")
        lines.append("")
        lines.append("Run: [bold]/agent <role> <prompt>[/]")
        log.write("\n".join(lines))

    def action_clear_chat(self) -> None:
        self.orchestrator.session.clear()
        log = self.query_one("#chat", RichLog)
        log.clear()
        log.write("[#6fdc6f dim]Conversation cleared.[/]")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if self._busy:
            return

        text = event.value.strip()
        event.input.value = ""
        if not text:
            return

        log = self.query_one("#chat", RichLog)
        command = parse_slash_command(text)
        if command is not None:
            if command.action is SlashAction.QUIT:
                self.exit()
                return
            if command.action is SlashAction.HELP:
                log.write(HELP_TEXT)
                return
            if command.action is SlashAction.CLEAR:
                self.action_clear_chat()
                return
            if command.action is SlashAction.LIST_AGENTS:
                self._write_agent_catalog(log)
                return
            if command.action is SlashAction.AGENT_HELP:
                log.write(f"[#8dff8d]{command.message}[/]")
                self._write_agent_catalog(log)
                return
            if command.action is SlashAction.UNKNOWN:
                log.write(f"[bold red]{command.message}[/]")
                return
            if command.action is SlashAction.RUN_AGENT:
                assert command.agent_role is not None
                assert command.agent_prompt is not None
                await self._run_agent_turn(log, command.agent_role, command.agent_prompt)
                return
            if command.action is SlashAction.FLOW_HELP:
                log.write(f"[#8dff8d]{command.message}[/]")
                return
            if command.action is SlashAction.RUN_FLOW:
                assert command.agent_prompt is not None
                await self._run_flow_turn(log, command.agent_prompt)
                return
            if command.action is SlashAction.CHAT_HELP:
                log.write(f"[#8dff8d]{command.message}[/]")
                return
            if command.action is SlashAction.RUN_CHAT:
                assert command.agent_prompt is not None
                await self._run_chat_turn(log, command.agent_prompt)
                return

        await self._run_flow_turn(log, text)

    async def _run_agent_turn(self, log: RichLog, role: AgentRole, prompt: str) -> None:
        self._set_busy(True)
        title = role.value.replace("-", " ").title()
        try:
            log.write(f"[bold #7dffb8]You[/] · [dim]/agent {role.value}[/]\n{prompt}")
            on_phase, on_stream = self._begin_work(
                f"Agent · {title}",
                f"Streaming · {title}",
            )

            def run_agent() -> str:
                return self.orchestrator.invoke_agent(
                    role,
                    prompt,
                    on_phase=on_phase,
                    on_stream=on_stream,
                )

            reply = await asyncio.to_thread(run_agent)
            write_assistant_markdown(
                log,
                f"[bold #43ff43]🤖 {title}[/]:",
                reply,
            )
        except GeminiRequestError as exc:
            log.write(_format_provider_error(exc))
        except ValueError as exc:
            log.write(f"[bold red]Input error[/]: {exc}")
        finally:
            self._end_work()
            self._set_busy(False)
            self.query_one("#prompt", Input).focus()

    async def _run_flow_turn(self, log: RichLog, prompt: str) -> None:
        self._set_busy(True)
        try:
            log.write(f"[bold #7dffb8]You[/] · [dim]QA flow[/]\n{prompt}")
            on_phase, on_stream = self._begin_work(
                "Agent · QA flow",
                "Streaming · multi-agent output",
            )

            def run_flow() -> str:
                return self.orchestrator.invoke_qa_flow(
                    prompt,
                    on_phase=on_phase,
                    on_stream=on_stream,
                )

            reply = await asyncio.to_thread(run_flow)
            write_assistant_markdown(log, "[bold #43ff43]🤖 Multi-agent QA flow[/]:", reply)
        except GeminiRequestError as exc:
            log.write(_format_provider_error(exc))
        except ValueError as exc:
            log.write(f"[bold red]Input error[/]: {exc}")
        finally:
            self._end_work()
            self._set_busy(False)
            self.query_one("#prompt", Input).focus()

    async def _run_chat_turn(self, log: RichLog, text: str) -> None:
        self._set_busy(True)
        try:
            log.write(f"[bold #7dffb8]You[/]: {text}")
            on_phase, on_stream = self._begin_work(
                "Tool · gemini-reasoning",
                "Streaming · QA advisor",
            )

            def run_chat() -> str:
                on_phase("Tool · gemini-reasoning")
                return self.orchestrator.respond_chat(text, on_stream=on_stream)

            reply = await asyncio.to_thread(run_chat)
            write_assistant_markdown(log, "[bold #43ff43]QA Engineer[/]:", reply)
        except GeminiRequestError as exc:
            log.write(_format_provider_error(exc))
        except ValueError as exc:
            log.write(f"[bold red]Input error[/]: {exc}")
        finally:
            self._end_work()
            self._set_busy(False)
            self.query_one("#prompt", Input).focus()


def main() -> int:
    load_project_dotenv()
    try:
        client = GeminiChatClient()
        session = QualityEngineerSession(client)
        orchestrator = QATUIOrchestrator(session)
    except GeminiConfigurationError as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("Set GEMINI_API_KEY in .env or your shell, then retry.", file=sys.stderr)
        return 2

    QAEngineerApp(orchestrator).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
