from __future__ import annotations

import os
from dataclasses import dataclass

from ticket_insight.providers import get_provider_metadata


@dataclass(frozen=True)
class ProviderKeyResolution:
    provider: str
    env_var: str
    api_key: str | None
    source: str | None

    @property
    def is_available(self) -> bool:
        return self.api_key is not None


def get_env_api_key(provider: str) -> str | None:
    metadata = get_provider_metadata(provider)
    return _normalize_api_key(os.getenv(metadata.env_var))


def resolve_provider_api_key(
    provider: str,
    session_api_key: str | None = None,
) -> ProviderKeyResolution:
    metadata = get_provider_metadata(provider)
    env_api_key = _normalize_api_key(os.getenv(metadata.env_var))
    if env_api_key is not None:
        return ProviderKeyResolution(
            provider=metadata.name,
            env_var=metadata.env_var,
            api_key=env_api_key,
            source="environment",
        )

    normalized_session_key = _normalize_api_key(session_api_key)
    if normalized_session_key is not None:
        return ProviderKeyResolution(
            provider=metadata.name,
            env_var=metadata.env_var,
            api_key=normalized_session_key,
            source="session",
        )

    return ProviderKeyResolution(
        provider=metadata.name,
        env_var=metadata.env_var,
        api_key=None,
        source=None,
    )


def _normalize_api_key(api_key: str | None) -> str | None:
    if api_key is None:
        return None

    normalized = api_key.strip()
    return normalized or None
