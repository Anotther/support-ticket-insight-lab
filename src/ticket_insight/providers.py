from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_PROVIDERS: tuple[str, ...] = ("openai", "gemini", "groq")


@dataclass(frozen=True)
class ProviderMetadata:
    name: str
    label: str
    env_var: str
    models: list[str]
    request_interval_s: float  # seconds between requests, safe for free-tier RPM limits


PROVIDER_METADATA: dict[str, ProviderMetadata] = {
    "openai": ProviderMetadata(
        name="openai",
        label="OpenAI",
        env_var="OPENAI_API_KEY",
        models=["gpt-4o-mini", "gpt-3.5-turbo"],
        request_interval_s=20.0,
    ),
    "gemini": ProviderMetadata(
        name="gemini",
        label="Gemini",
        env_var="GEMINI_API_KEY",
        models=["gemini-1.5-flash", "gemini-1.5-pro"],
        request_interval_s=4.1,
    ),
    "groq": ProviderMetadata(
        name="groq",
        label="Groq",
        env_var="GROQ_API_KEY",
        models=["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
        request_interval_s=2.1,
    ),
}


def get_provider_metadata(provider: str) -> ProviderMetadata:
    try:
        return PROVIDER_METADATA[provider]
    except KeyError as exc:
        supported = ", ".join(SUPPORTED_PROVIDERS)
        message = f"Unsupported provider '{provider}'. Supported providers: {supported}."
        raise ValueError(message) from exc
