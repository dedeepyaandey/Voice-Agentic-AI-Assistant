"""Voice input and output utilities."""

from __future__ import annotations

from config import settings


def listen_from_microphone(timeout: int = 5, phrase_time_limit: int = 10) -> str:
    try:
        import speech_recognition as sr
    except ImportError:
        raise RuntimeError("SpeechRecognition is not installed. Use text mode or install requirements.")

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError as exc:
        raise RuntimeError("Could not understand the audio.") from exc
    except sr.RequestError as exc:
        raise RuntimeError(f"Speech recognition service failed: {exc}") from exc


def speak(text: str) -> None:
    if not settings.tts_enabled:
        return
    try:
        import pyttsx3
    except ImportError:
        return

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
