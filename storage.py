"""CSV persistence helpers."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from config import CONVERSATION_CSV, DATA_DIR, NOTES_CSV, TASKS_CSV


CONVERSATION_FIELDS = [
    "timestamp",
    "transcript",
    "response",
    "intent",
    "category",
    "emails",
    "phones",
    "dates",
    "keywords",
]
NOTES_FIELDS = ["timestamp", "note"]
TASKS_FIELDS = ["timestamp", "task", "status", "due_date"]


def initialize_storage() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    _ensure_csv(CONVERSATION_CSV, CONVERSATION_FIELDS)
    _ensure_csv(NOTES_CSV, NOTES_FIELDS)
    _ensure_csv(TASKS_CSV, TASKS_FIELDS)


def _ensure_csv(path: Path, fields: list[str]) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()


def append_conversation(
    transcript: str,
    response: str,
    intent: str,
    category: str,
    entities: dict[str, list[str]],
) -> None:
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "transcript": transcript,
        "response": response,
        "intent": intent,
        "category": category,
        "emails": "; ".join(entities.get("emails", [])),
        "phones": "; ".join(entities.get("phones", [])),
        "dates": "; ".join(entities.get("dates", [])),
        "keywords": "; ".join(entities.get("keywords", [])),
    }
    _append_row(CONVERSATION_CSV, CONVERSATION_FIELDS, row)


def append_note(note: str) -> None:
    _append_row(
        NOTES_CSV,
        NOTES_FIELDS,
        {"timestamp": datetime.now().isoformat(timespec="seconds"), "note": note},
    )


def append_task(task: str, due_date: str = "") -> None:
    _append_row(
        TASKS_CSV,
        TASKS_FIELDS,
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "task": task,
            "status": "open",
            "due_date": due_date,
        },
    )


def load_tasks(status: str | None = None) -> list[dict[str, str]]:
    initialize_storage()
    with TASKS_CSV.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if status:
        rows = [row for row in rows if row["status"].lower() == status.lower()]
    return sorted(rows, key=lambda row: (row.get("due_date") or "9999-99-99", row["timestamp"]))


def search_conversations(term: str) -> list[dict[str, str]]:
    initialize_storage()
    needle = term.lower()
    with CONVERSATION_CSV.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row
        for row in rows
        if needle in row["transcript"].lower() or needle in row["response"].lower()
    ]


def _append_row(path: Path, fields: list[str], row: dict[str, Any]) -> None:
    initialize_storage()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writerow(row)
