from ticket_insight.providers import PROVIDER_METADATA, SUPPORTED_PROVIDERS, get_provider_metadata


def test_supported_providers_are_preserved() -> None:
    assert SUPPORTED_PROVIDERS == ("openai", "gemini", "groq")


def test_all_supported_providers_have_label_and_env_var() -> None:
    for provider in SUPPORTED_PROVIDERS:
        metadata = get_provider_metadata(provider)

        assert metadata.name == provider
        assert metadata.label
        assert metadata.env_var == f"{provider.upper()}_API_KEY"
        assert PROVIDER_METADATA[provider] == metadata
