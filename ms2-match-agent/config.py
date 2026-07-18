"""
Centralized configuration for MS2.

Every environment variable the service needs is read exactly once, in
exactly one place. Nothing else in the codebase should call os.getenv()
directly — that keeps config lookups from being scattered across files,
so there's a single source of truth for what MS2 needs to run.
"""
import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add it to a .env file in the "
        "project root (see .env.example) — never hardcode it in source."
    )
print("MODEL =", GEMINI_MODEL)
