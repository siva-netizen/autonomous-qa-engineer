"""Thread-local streaming callback for TUI token previews during Gemini calls."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar, Token

StreamCallback = Callable[[str], None]

_stream_callback: ContextVar[StreamCallback | None] = ContextVar(
    "gemini_stream_callback",
    default=None,
)


def get_stream_callback() -> StreamCallback | None:
    return _stream_callback.get()


@contextmanager
def stream_callback_scope(callback: StreamCallback | None) -> Iterator[None]:
    if callback is None:
        yield
        return
    token: Token[StreamCallback | None] = _stream_callback.set(callback)
    try:
        yield
    finally:
        _stream_callback.reset(token)
