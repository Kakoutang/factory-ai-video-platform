from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ASSET_ROOT = BASE_DIR / "data" / "client-assets"


def asset_root() -> Path:
    configured = os.getenv("CLIENT_ASSET_ROOT")
    root = Path(configured).expanduser() if configured else DEFAULT_ASSET_ROOT
    root.mkdir(parents=True, exist_ok=True)
    return root


def cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "*")
    if raw.strip() == "*":
        return ["*"]
    return [item.strip() for item in raw.split(",") if item.strip()]
