"""Format structured agent results for CLI and TUI output."""

from __future__ import annotations

import json

from agents.contracts import AgentResult


def format_agent_result(result: AgentResult) -> str:
    output = result.output
    if output is None:
        return result.content

    title = output.role.value.replace("-", " ").title()
    lines = [
        f"### Agent · {title}",
        f"`{result.request_id}` · lifecycle `{output.lifecycle.value}`",
        "",
        output.summary,
    ]
    written = result.metadata.get("written_test_path")
    if isinstance(written, str):
        lines.extend(["", f"**Artifact:** `{written}`"])
    if output.open_questions:
        lines.extend(["", "**Open questions**", *[f"- {item}" for item in output.open_questions]])
    if output.assumptions:
        lines.extend(["", "**Assumptions**", *[f"- {item}" for item in output.assumptions]])
    payload = json.dumps(dict(output.payload), indent=2, sort_keys=True, default=str)
    lines.extend(["", "**Payload**", f"```json\n{payload}\n```"])
    return "\n".join(lines)
