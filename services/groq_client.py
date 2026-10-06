"""Deprecated compatibility aliases for the former Groq adapter.

Use :mod:`services.gemini_client` and ``GEMINI_*`` environment variables for
all new code. The aliases remain only to avoid breaking external imports while
this repository migrates providers.
"""

from services.gemini_client import (
    ChatCompletion,
    ChatMessage,
    ChatTransport,
    GeminiChatClient,
    GeminiConfig,
    GeminiConfigurationError,
    GeminiRequestError,
    ReasoningClient,
    UrllibChatTransport,
)

GroqConfig = GeminiConfig
GroqConfigurationError = GeminiConfigurationError
GroqRequestError = GeminiRequestError


class GroqChatClient(GeminiChatClient):
    """Deprecated alias; reads Gemini configuration, not Groq variables."""


__all__ = [
    "ChatCompletion",
    "ChatMessage",
    "ChatTransport",
    "GroqChatClient",
    "GroqConfig",
    "GroqConfigurationError",
    "GroqRequestError",
    "ReasoningClient",
    "UrllibChatTransport",
]
