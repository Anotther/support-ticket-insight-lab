import pytest

from ticket_insight.config import get_env_api_key, resolve_provider_api_key


def test_get_env_api_key_uses_provider_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")

    assert get_env_api_key("openai") == "env-key"


def test_env_key_takes_precedence_over_session_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "env-key")

    resolution = resolve_provider_api_key("gemini", session_api_key="session-key")

    assert resolution.provider == "gemini"
    assert resolution.env_var == "GEMINI_API_KEY"
    assert resolution.api_key == "env-key"
    assert resolution.source == "environment"
    assert resolution.is_available


def test_session_key_is_used_when_env_key_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    resolution = resolve_provider_api_key("groq", session_api_key=" session-key ")

    assert resolution.provider == "groq"
    assert resolution.env_var == "GROQ_API_KEY"
    assert resolution.api_key == "session-key"
    assert resolution.source == "session"
    assert resolution.is_available


def test_missing_env_and_session_key_returns_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    resolution = resolve_provider_api_key("openai", session_api_key=" ")

    assert resolution.provider == "openai"
    assert resolution.env_var == "OPENAI_API_KEY"
    assert resolution.api_key is None
    assert resolution.source is None
    assert not resolution.is_available


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported provider"):
        resolve_provider_api_key("unknown")
