"""LLM integration with Gemini, Ollama, and a deterministic fallback."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from config import settings


SYSTEM_PROMPT = (
    "You are a concise, helpful voice assistant. Answer in 2-4 sentences. "
    "If the user asks for steps, use a short numbered list."
)


def generate_response(prompt: str, context: str = "") -> str:
    provider = settings.llm_provider
    if provider == "gemini":
        return _gemini_response(prompt, context)
    if provider == "ollama":
        return _ollama_response(prompt, context)
    return _fallback_response(prompt, context)


def _gemini_response(prompt: str, context: str) -> str:
    if not settings.gemini_api_key:
        return _fallback_response(prompt, context, "Gemini API key is missing.")

    try:
        import google.generativeai as genai
    except ImportError:
        return _fallback_response(prompt, context, "google-generativeai is not installed.")

    try:
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(settings.gemini_model)
        result = model.generate_content(f"{SYSTEM_PROMPT}\n\nContext: {context}\n\nUser: {prompt}")
        return (result.text or "").strip() or _fallback_response(prompt, context)
    except Exception as exc:
        return _fallback_response(prompt, context, f"Gemini failed: {exc}")


def _ollama_response(prompt: str, context: str) -> str:
    payload = {
        "model": settings.ollama_model,
        "prompt": f"{SYSTEM_PROMPT}\n\nContext: {context}\n\nUser: {prompt}",
        "stream": False,
    }
    try:
        request = urllib.request.Request(
            f"{settings.ollama_host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("response", "").strip() or _fallback_response(prompt, context)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return _fallback_response(prompt, context, f"Ollama failed: {exc}")


def _fallback_response(prompt: str, context: str = "", reason: str = "") -> str:
    prefix = f"{reason} " if reason else ""
    if context:
        return f"{prefix}I understood your request and found this context: {context}. For '{prompt}', I recommend breaking it into the next clear action and tracking it."
    return f"{prefix}I understood: '{prompt}'. I can help save notes, add tasks, summarize text, extract emails/phones/dates, and search conversation history."
