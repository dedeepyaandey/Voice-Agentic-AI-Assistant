# Voice Agentic AI Assistant

Python implementation for the hackathon problem statement.

## Features

- Voice-to-text with `SpeechRecognition`
- Text-to-voice with `pyttsx3`
- Regex extraction for greetings, dates, emails, phone numbers, keywords, and commands
- Agentic routing for notes, tasks, summaries, search, and entity extraction
- Gemini or Ollama integration with a deterministic fallback response mode
- CSV persistence for conversations, notes, and tasks

## Run

Text mode works without microphone or API keys:

```bash
python3 main.py --mode text
```

Voice mode requires microphone dependencies:

```bash
python3 -m pip install -r requirements.txt
python3 main.py --mode voice
```

## Optional LLM Setup

Gemini:

```bash
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=your_api_key
python3 main.py --mode text
```

Ollama:

```bash
ollama pull llama3.1
export LLM_PROVIDER=ollama
python3 main.py --mode text
```

## Demo Commands

```text
hello
save note meet the project team at 5 PM
add task submit hackathon demo by tomorrow
show today's tasks
summarize Python is a programming language used for AI and automation.
My email is test@example.com and phone number is 9876543210
search hackathon
```

CSV files are created in `data/`:

- `conversations.csv`
- `notes.csv`
- `tasks.csv`
