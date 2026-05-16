"""Application configuration for the Voice Agentic AI Assistant."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CONVERSATION_CSV = DATA_DIR / "conversations.csv"
NOTES_CSV = DATA_DIR / "notes.csv"
TASKS_CSV = DATA_DIR / "tasks.csv"


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "fallback").lower()
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    tts_enabled: bool = os.getenv("TTS_ENABLED", "true").lower() != "false"


settings = Settings()
