"""Agentic routing layer."""

from __future__ import annotations

from llm_client import generate_response
from storage import append_note, append_task, load_tasks, search_conversations
from text_processing import AnalysisResult


HELP_TEXT = (
    "Try commands like: save note remember to call Ravi, add task submit report by tomorrow, "
    "show today's tasks, summarize followed by your message, or search invoice."
)


def handle_intent(transcript: str, analysis: AnalysisResult) -> str:
    if analysis.intent == "empty":
        return "I did not receive any text. Please try again."

    if analysis.intent == "help":
        return HELP_TEXT

    if analysis.intent == "greeting":
        return "Hello. I am ready to help with notes, tasks, summaries, entity extraction, and general questions."

    if analysis.intent == "save_note":
        note = analysis.action_payload or transcript
        append_note(note)
        return f"Saved your note: {note}"

    if analysis.intent == "add_task":
        task = analysis.action_payload or transcript
        due_date = analysis.entities["dates"][0] if analysis.entities["dates"] else ""
        append_task(task, due_date)
        return f"Added task: {task}"

    if analysis.intent == "show_tasks":
        tasks = load_tasks(status="open")
        if not tasks:
            return "You do not have any open tasks yet."
        lines = [f"{index}. {task['task']}" for index, task in enumerate(tasks[:5], start=1)]
        return "Here are your open tasks: " + " ".join(lines)

    if analysis.intent == "search_history":
        term = analysis.action_payload
        matches = search_conversations(term)
        if not matches:
            return f"I could not find earlier conversations matching '{term}'."
        latest = matches[-3:]
        return "I found these recent matches: " + " | ".join(row["transcript"] for row in latest)

    if analysis.intent == "extract_entities":
        parts = []
        for label, values in analysis.entities.items():
            if values:
                parts.append(f"{label}: {', '.join(values)}")
        return "I extracted " + "; ".join(parts) + "."

    if analysis.intent == "summarize":
        target = analysis.action_payload or transcript
        return generate_response(f"Summarize this clearly: {target}", context="Summarization request")

    entity_context = _entity_context(analysis)
    return generate_response(transcript, context=entity_context)


def _entity_context(analysis: AnalysisResult) -> str:
    pieces = [f"intent={analysis.intent}", f"category={analysis.category}"]
    for name, values in analysis.entities.items():
        if values:
            pieces.append(f"{name}={', '.join(values)}")
    return "; ".join(pieces)
