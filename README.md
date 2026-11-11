# JARVIS Voice Assistant

A Python voice assistant that listens for spoken requests, reads responses aloud, and can answer general questions through Google's Gemini API.

## Features

- Speech recognition through a microphone
- Text-to-speech responses
- Current-time lookup
- Opens selected public websites
- Gemini-powered conversational responses

## Requirements

- Python 3.10+
- A working microphone and audio output
- A Gemini API key
- Platform audio libraries required by SpeechRecognition and PyAudio

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Set `GEMINI_API_KEY` in `.env`, load it into your shell, and launch:

```bash
set -a
. ./.env
set +a
python jarvis.py
```

## Security and privacy

The assistant sends recognized prompts to an external AI service. Do not speak or submit passwords, financial details, or other sensitive information. Keep API credentials private and rotate any key that has been committed to Git.

## Troubleshooting

- Check microphone permissions and operating-system audio support.
- Confirm that the virtual environment is active.
- Verify that `GEMINI_API_KEY` is set in the current shell.
