from __future__ import annotations

import os


def get_env_api_key(provider: str) -> str | None:
    key_name = f"{provider.upper()}_API_KEY"
    value = os.getenv(key_name)
    return value if value else None
