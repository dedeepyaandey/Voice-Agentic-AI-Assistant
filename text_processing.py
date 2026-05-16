"""Regex and pattern matching for transcripts."""

from __future__ import annotations

from dataclasses import dataclass
import re


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3,5}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{4}\b")
DATE_RE = re.compile(
    r"\b(?:today|tomorrow|yesterday|next\s+\w+|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
    r"\d{4}[/-]\d{1,2}[/-]\d{1,2}|"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:,\s*\d{4})?)\b",
    re.IGNORECASE,
)

GREETINGS_RE = re.compile(r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b", re.IGNORECASE)
SAVE_NOTE_RE = re.compile(r"\b(save|store|remember)\s+(?:this\s+)?note\b[:\s]*(.*)", re.IGNORECASE)
ADD_TASK_RE = re.compile(r"\b(add|create|save)\s+(?:a\s+)?task\b[:\s]*(.*)", re.IGNORECASE)
SHOW_TASKS_RE = re.compile(r"\b(show|list|display)\s+(?:today'?s\s+|my\s+)?tasks\b", re.IGNORECASE)
SUMMARIZE_RE = re.compile(r"\b(summarize|summary of)\b[:\s]*(.*)", re.IGNORECASE)
SEARCH_RE = re.compile(r"\b(search|find)\s+(?:for\s+)?(.+)", re.IGNORECASE)
HELP_RE = re.compile(r"\b(help|what can you do|commands)\b", re.IGNORECASE)

KEYWORDS = {
    "meeting",
    "email",
    "phone",
    "task",
    "note",
    "summary",
    "deadline",
    "appointment",
    "invoice",
    "reminder",
    "project",
}


@dataclass(frozen=True)
class AnalysisResult:
    intent: str
    category: str
    entities: dict[str, list[str]]
    action_payload: str = ""


def analyze_text(text: str) -> AnalysisResult:
    normalized = " ".join(text.strip().split())
    lowered = normalized.lower()

    entities = {
        "emails": EMAIL_RE.findall(normalized),
        "phones": [match.group(0).strip() for match in PHONE_RE.finditer(normalized)],
        "dates": [match.group(0) for match in DATE_RE.finditer(normalized)],
        "keywords": sorted(keyword for keyword in KEYWORDS if keyword in lowered),
    }

    if not normalized:
        return AnalysisResult("empty", "system", entities)

    save_note = SAVE_NOTE_RE.search(normalized)
    if save_note:
        return AnalysisResult("save_note", "productivity", entities, save_note.group(2).strip())

    add_task = ADD_TASK_RE.search(normalized)
    if add_task:
        return AnalysisResult("add_task", "productivity", entities, add_task.group(2).strip())

    if SHOW_TASKS_RE.search(normalized):
        return AnalysisResult("show_tasks", "productivity", entities)

    summarize = SUMMARIZE_RE.search(normalized)
    if summarize:
        return AnalysisResult("summarize", "language", entities, summarize.group(2).strip())

    search = SEARCH_RE.search(normalized)
    if search:
        return AnalysisResult("search_history", "analytics", entities, search.group(2).strip())

    if HELP_RE.search(normalized):
        return AnalysisResult("help", "system", entities)

    if GREETINGS_RE.search(normalized):
        return AnalysisResult("greeting", "conversation", entities)

    if entities["emails"] or entities["phones"] or entities["dates"]:
        return AnalysisResult("extract_entities", "data_extraction", entities)

    return AnalysisResult("general_query", "general", entities)
