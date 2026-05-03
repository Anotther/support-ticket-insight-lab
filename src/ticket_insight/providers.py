from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_PROVIDERS: tuple[str, ...] = ("openai", "gemini", "groq")


@dataclass(frozen=True)
class ProviderMetadata:
    name: str
    label: str
    env_var: str


PROVIDER_METADATA: dict[str, ProviderMetadata] = {
    "openai": ProviderMetadata(name="openai", label="OpenAI", env_var="OPENAI_API_KEY"),
    "gemini": ProviderMetadata(name="gemini", label="Gemini", env_var="GEMINI_API_KEY"),
    "groq": ProviderMetadata(name="groq", label="Groq", env_var="GROQ_API_KEY"),
}


def get_provider_metadata(provider: str) -> ProviderMetadata:
    try:
        return PROVIDER_METADATA[provider]
    except KeyError as exc:
        supported = ", ".join(SUPPORTED_PROVIDERS)
        message = f"Unsupported provider '{provider}'. Supported providers: {supported}."
        raise ValueError(message) from exc
