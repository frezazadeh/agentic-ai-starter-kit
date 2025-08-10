from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI


@dataclass(frozen=True)
class Settings:
    api_key: str
    model_default: str
    model_fast: str
    model_tiny: str


def load_settings() -> Settings:
    # Load once at import time so CLI tools “just work”
    load_dotenv(override=True)

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Create .env from .env.example and fill it in.")

    return Settings(
        api_key=api_key,
        model_default=os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4.1"),
        model_fast=os.getenv("OPENAI_FAST_MODEL", "gpt-4.1-mini"),
        model_tiny=os.getenv("OPENAI_TINY_MODEL", "gpt-4.1-nano"),
    )


def make_client(settings: Settings) -> OpenAI:
    # The official SDK picks up the key from env automatically,
    # but we construct and return a client explicitly for clarity.
    return OpenAI(api_key=settings.api_key)
