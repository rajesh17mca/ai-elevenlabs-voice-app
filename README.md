# ElevenLabs Studio

A production-grade web application for **Text to Speech** and **Speech to Text** conversion powered by the [ElevenLabs API](https://elevenlabs.io).

## Features

- **Text to Speech** — Enter any text, generate high-quality AI audio, play it directly in the browser, and download as MP3.
- **Speech to Text** — Upload an audio file (drag & drop or browse), transcribe it using ElevenLabs Scribe, and download the transcript as TXT.
- No extra web framework required — built on Python's stdlib `http.server`.

## Project Structure

```
elevenlabs_learning/
├── app.py              # Production web app (HTTP server + UI)
├── streamlit_app.py    # Streamlit web app (alternative UI)
├── main.py             # CLI script for quick TTS + STT testing
├── pyproject.toml
├── uv.lock
└── .env                # API keys (not committed)
```

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- An [ElevenLabs API key](https://elevenlabs.io/app/settings/api-keys)

## Setup

**1. Clone the repository**

```bash
git clone <repo-url>
cd elevenlabs_learning
```

**2. Create a virtual environment and install dependencies**

```bash
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install elevenlabs python-dotenv
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```env
ELEVENLABS_API_KEY=your_api_key_here
```

## Usage

### Streamlit App (Recommended)

```bash
uv run streamlit run streamlit_app.py
```

Open the provided URL in your browser (usually [http://localhost:8501](http://localhost:8501)).

| Tab | How to use |
|-----|-----------|
| **Text to Speech** | Type or paste text → click **Convert to Speech** → play or download the MP3 |
| **Speech to Text** | Upload an audio file → click **Transcribe Audio** → read or download the TXT |

### Web App (Alternative)

```bash
.venv/bin/python app.py
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

| Tab | How to use |
|-----|-----------|
| **Text to Speech** | Type or paste text → click **Convert to Speech** → play or download the MP3 |
| **Speech to Text** | Drag & drop or upload an audio file → click **Transcribe Audio** → read or download the TXT |

To run on a different port:

```bash
PORT=9000 .venv/bin/python app.py
```

### CLI Script

For quick testing from the terminal:

```bash
.venv/bin/python main.py
```

This converts a hardcoded sample sentence to speech, plays it, then transcribes it back to text and prints the result.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/`       | Serves the web UI |
| `POST` | `/api/tts` | Convert text to speech. Body: `{"text": "..."}`. Returns `audio/mpeg`. |
| `POST` | `/api/stt` | Transcribe audio to text. Body: `multipart/form-data` with `file` field. Returns `{"text": "..."}`. |

## Configuration

The following constants in `app.py` can be adjusted:

| Constant | Default | Description |
|----------|---------|-------------|
| `VOICE_ID` | `JBFqnCBsd6RMkjVDRZzb` | ElevenLabs voice ID (George) |
| `TTS_MODEL` | `eleven_v3` | Text-to-speech model |
| `STT_MODEL` | `scribe_v1` | Speech-to-text model |

Browse available voices at [elevenlabs.io/app/voice-library](https://elevenlabs.io/app/voice-library).

## Supported Audio Formats

MP3, WAV, M4A, OGG, FLAC, MP4 (and most other audio/video formats supported by ElevenLabs Scribe).

## Dependencies

| Package | Purpose |
|---------|---------|
| `elevenlabs` | ElevenLabs Python SDK |
| `python-dotenv` | Load API keys from `.env` |
| `streamlit` | Web app framework (for streamlit_app.py) |
