"""Voice Agentic AI Assistant entry point."""

from __future__ import annotations

import argparse

from agent import handle_intent
from storage import append_conversation, initialize_storage
from text_processing import analyze_text
from voice_io import listen_from_microphone, speak


def process_transcript(transcript: str, speak_response: bool = True) -> str:
    analysis = analyze_text(transcript)
    response = handle_intent(transcript, analysis)
    append_conversation(
        transcript=transcript,
        response=response,
        intent=analysis.intent,
        category=analysis.category,
        entities=analysis.entities,
    )
    print(f"\nUser: {transcript}")
    print(f"Intent: {analysis.intent} | Category: {analysis.category}")
    print(f"Assistant: {response}\n")
    if speak_response:
        speak(response)
    return response


def run_text_mode() -> None:
    print("Voice Agentic AI Assistant - text mode")
    print("Type 'exit' to quit. Type 'help' for command examples.\n")
    while True:
        transcript = input("You: ").strip()
        if transcript.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        process_transcript(transcript)


def run_voice_mode() -> None:
    print("Voice Agentic AI Assistant - voice mode")
    print("Say 'exit' or 'quit' to stop.\n")
    while True:
        try:
            transcript = listen_from_microphone()
        except RuntimeError as exc:
            print(f"Voice input error: {exc}")
            break
        if transcript.lower().strip() in {"exit", "quit"}:
            print("Goodbye.")
            speak("Goodbye.")
            break
        process_transcript(transcript)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Voice Agentic AI Assistant")
    parser.add_argument(
        "--mode",
        choices=["text", "voice"],
        default="text",
        help="Use text mode for demo/fallback or voice mode for microphone input.",
    )
    return parser.parse_args()


def main() -> None:
    initialize_storage()
    args = parse_args()
    if args.mode == "voice":
        run_voice_mode()
    else:
        run_text_mode()


if __name__ == "__main__":
    main()
