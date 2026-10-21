# 🎬 YouTube AI Automation

> **From niche to published YouTube Short — fully automated.**
> Enter a topic. AI generates the idea, writes the script, records the voiceover, sources footage, burns subtitles, renders the video, and uploads it to YouTube.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange?logo=google)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Project Structure](#3-project-structure)
4. [Technology Stack](#4-technology-stack)
5. [Service Explanations](#5-service-explanations)
6. [API Reference](#6-api-reference)
7. [Build From Scratch — Development Roadmap](#7-build-from-scratch--development-roadmap)
8. [File Dependency Map](#8-file-dependency-map)
9. [Configuration Files](#9-configuration-files)
10. [Security Analysis](#10-security-analysis)
11. [Scalability & Future Improvements](#11-scalability--future-improvements)
12. [Challenges & Solutions](#12-challenges--solutions)
13. [Quick Start](#13-quick-start)
14. [Final Summary](#14-final-summary)

---

## 1. Project Overview

### What Is This?

YouTube AI Automation is a full-stack, end-to-end pipeline that takes one user input — a content niche — and produces a complete, published YouTube Shorts video. No manual editing. No separate tools. One input, one button, one published video.

### Problem Statement

Creating YouTube Shorts manually requires expertise across multiple domains:

| Manual Step | Time Cost |
|---|---|
| Content ideation & research | 30–60 min |
| Scriptwriting | 30–45 min |
| Voice recording / editing | 20–40 min |
| Video editing & sourcing footage | 60–90 min |
| Subtitle creation | 20–30 min |
| Publishing & metadata | 10–15 min |
| **Total per video** | **~3–5 hours** |

This project compresses all of that into a single button click.

### Target Users

| User | Their Need |
|---|---|
| Content Creators | Scale video output without hiring a team |
| YouTubers | Maintain consistent upload schedules automatically |
| Digital Marketers | Generate promotional Shorts at scale |
| Social Media Agencies | Manage multiple channels efficiently |
| Small Businesses | Create educational/promotional content cheaply |
| AI Enthusiasts | Learn modern AI pipeline architecture in practice |

### Key Objectives

1. Automate idea generation using Google Gemini AI
2. Generate structured voiceover scripts automatically
3. Convert script to natural speech using Kokoro TTS
4. Source relevant stock footage from Pixabay API
5. Generate and burn subtitles into the final video
6. Render complete videos using MoviePy and FFmpeg
7. Upload directly to YouTube via the Data API v3
8. Show real-time pipeline progress in a web UI

---

## 2. System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────┐
│              USER BROWSER (Frontend)            │
│  HTML + CSS + JS  →  /templates/index.html      │
│  Input: Niche Topic  →  POST /api/generate      │
└──────────────────────────┬──────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────┐
│           FASTAPI BACKEND (app/main.py)         │
│  Routes → Services → Pipeline Orchestration     │
└──────────────────────────┬──────────────────────┘
                           │
┌──────────────────────────▼──────────────────────┐
│        PIPELINE SERVICE (Orchestrator)          │
├──────────┬──────────┬──────────┬────────────────┤
│  Idea    │  Script  │  Voice   │  Stock Video   │
│ Service  │ Service  │ Service  │  Service       │
├──────────┴──────────┴──────────┴────────────────┤
│       Subtitle  │   Video   │   YouTube        │
│        Service  │  Service  │   Service        │
└────────┬────────┴─────┬─────┴─────────────────┘
         │              │
  [Gemini AI]   [Pixabay API + FFmpeg + YouTube API]
```

### Data Flow — Step by Step

| Stage | Transformation |
|---|---|
| 1 | User enters niche → HTTP POST to `/api/generate` |
| 2 | `idea_service` → Gemini generates JSON idea (title, hook, keywords) |
| 3 | `script_service` → Gemini generates full narration script |
| 4 | `voice_service` → Kokoro TTS converts script to MP3 audio |
| 5 | `stock_video_service` → Downloads relevant MP4 clips from Pixabay |
| 6 | `subtitle_service` → Generates timed `.SRT` subtitle file |
| 7 | `video_service` → MoviePy assembles clips + audio → raw MP4 |
| 8 | `video_service` → FFmpeg burns subtitles into video → final MP4 |
| 9 | `youtube_service` → Uploads final MP4 to YouTube, returns URL |
| 10 | `pipeline_service` → Returns video path + YouTube URL to frontend |

### Request-Response Lifecycle

```
Browser  →  POST /api/generate {"niche": "fitness tips"}
           ↓
FastAPI Router (content.py)
           ↓
pipeline_service.run_pipeline("fitness tips")
           ↓
idea → script → audio → clips → subtitles → video → upload
           ↓
{"video_path": "artifacts/rendered_videos/abc.mp4",
 "youtube_url": "https://youtube.com/watch?v=XYZ"}
           ↓
Browser plays video + shows YouTube link
```

---

## 3. Project Structure

```
Youtube_AI_Automation/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── content.py          # POST /api/generate endpoint
│   │       └── youtube.py          # YouTube OAuth callback routes
│   │
│   ├── core/
│   │   ├── config.py               # Load .env → Settings object
│   │   └── logger.py               # App-wide logging configuration
│   │
│   ├── schemas/
│   │   └── request_schema.py       # Pydantic request/response models
│   │
│   ├── services/
│   │   ├── gemini_service.py       # ★ Google Gemini AI gateway
│   │   ├── idea_service.py         # Pipeline Step 1: idea generation
│   │   ├── script_service.py       # Pipeline Step 2: script writing
│   │   ├── voice_service.py        # Pipeline Step 3: text-to-speech
│   │   ├── stock_video_service.py  # Pipeline Step 4: Pixabay footage
│   │   ├── subtitle_service.py     # Pipeline Step 5: SRT generation
│   │   ├── video_service.py        # Pipeline Steps 6+7: render + burn
│   │   ├── youtube_service.py      # Pipeline Step 8: upload
│   │   └── pipeline_service.py     # ★ Orchestrates all 8 steps
│   │
│   ├── templates/
│   │   └── index.html              # Frontend UI (Jinja2 template)
│   │
│   ├── static/
│   │   ├── css/                    # Frontend stylesheets
│   │   └── js/                     # Frontend JavaScript
│   │
│   ├── utils/
│   │   ├── ffmpeg_utils.py         # FFmpeg subprocess helpers
│   │   └── helpers.py              # Shared utility functions
│   │
│   └── main.py                     # FastAPI app entry point
│
├── artifacts/                      # ⚠️ Runtime-generated, not committed
│   ├── audio/                      # MP3 files from Kokoro TTS
│   ├── stock_videos/               # MP4 clips from Pixabay
│   ├── subtitles/                  # .SRT subtitle files
│   └── rendered_videos/            # Final output videos
│
├── tests/                          # Pytest unit + integration tests
├── .env                            # ⚠️ Secret API keys — never commit
├── .gitignore
├── requirements.txt
└── README.md
```

### Key Files at a Glance

| File | Role | Critical? |
|---|---|---|
| `pipeline_service.py` | Orchestrates all 8 pipeline steps | ★ Essential |
| `gemini_service.py` | Single gateway for all AI calls | ★ Essential |
| `video_service.py` | MoviePy + FFmpeg video assembly | ★ Essential |
| `main.py` | FastAPI app initialization | ★ Essential |
| `config.py` | Loads all API keys from `.env` | ★ Essential |
| `idea_service.py` | Step 1 — AI idea generation | Essential |
| `script_service.py` | Step 2 — AI script writing | Essential |
| `voice_service.py` | Step 3 — Text-to-speech | Essential |
| `stock_video_service.py` | Step 4 — Pixabay footage | Essential |
| `subtitle_service.py` | Step 5 — SRT generation | Essential |
| `youtube_service.py` | Step 8 — YouTube upload | Essential |
| `ffmpeg_utils.py` | FFmpeg subprocess wrappers | Supporting |
| `helpers.py` | Shared utility functions | Supporting |
| `request_schema.py` | API input/output validation | Supporting |
| `logger.py` | Consistent logging across services | Supporting |

---

## 4. Technology Stack

### Why Each Technology Was Chosen

| Technology | Role | Why Chosen | Alternative |
|---|---|---|---|
| **Python 3.11** | Core language | Best AI/ML ecosystem, clean syntax | — |
| **FastAPI** | Backend framework | Async, auto-docs at `/docs`, Pydantic built-in | Flask (slower, no auto-validation) |
| **Google Gemini 2.0 Flash** | AI content generation | Fast, cheap, strong JSON instruction-following | GPT-4, Claude |
| **Kokoro TTS** | Text-to-speech | Free, open-source, natural voice quality | ElevenLabs (paid), gTTS (robotic) |
| **MoviePy** | Video assembly | Python-native video editing API | OpenCV (lower level) |
| **FFmpeg** | Subtitle burning + encoding | Industry standard, handles what MoviePy can't | — |
| **imageio-ffmpeg** | Bundled FFmpeg binary | No manual OS install needed | System FFmpeg |
| **Pixabay API** | Stock footage | Free, royalty-free, reliable API | Pexels, Unsplash Video |
| **YouTube Data API v3** | Video upload | Official API, OAuth 2.0 | — |
| **Pydantic** | Data validation | Built into FastAPI, eliminates boilerplate | Marshmallow |
| **python-dotenv** | Config loading | Simple `.env` file parsing | os.environ directly |
| **Pytest** | Testing | Standard Python testing framework | unittest |
| **Jinja2** | HTML templating | Built into FastAPI for server-side rendering | React, Vue (overkill for MVP) |

---

## 5. Service Explanations

### `gemini_service.py` — The AI Gateway

**Design Pattern:** Adapter — wraps an external API behind your own interface.

```python
# All AI calls in the entire project flow through this one function
def generate(prompt: str) -> str:
    response = gemini_client.generate_content(prompt)
    return response.text
```

> **Why centralize it?** If Google changes their API, you fix one file — not six.

---

### `idea_service.py` — Step 1

Builds a prompt asking Gemini to think like a YouTube Shorts strategist. Returns structured JSON:

```json
{
  "title": "5 Python Tips That 10x Your Productivity",
  "hook": "Most developers waste 2 hours a day on code they don't need to write...",
  "keywords": ["python", "programming", "productivity"],
  "target_audience": "beginner to intermediate Python developers"
}
```

---

### `script_service.py` — Step 2

Takes the idea JSON and prompts Gemini to write a 60-second narration script. Specifies: conversational tone, 150–200 words, starts with the hook, ends with a call-to-action.

---

### `voice_service.py` — Step 3

Passes the script string to Kokoro TTS. Saves the output to `artifacts/audio/{uuid}.mp3`. The UUID filename prevents conflicts when multiple videos are generated simultaneously.

---

### `stock_video_service.py` — Step 4

Iterates over keywords from the idea JSON, makes Pixabay API search calls, and downloads MP4 clips per keyword. Includes validation: skips corrupt/empty clips, handles network errors gracefully.

---

### `subtitle_service.py` — Step 5

Reads the script text and audio duration. Splits the script into 8–12 word chunks and distributes timestamps evenly across the audio length. Writes a standard `.SRT` file understood by FFmpeg.

---

### `video_service.py` — Steps 6 & 7

**Phase 1 (MoviePy):** Loads each stock clip at a bounded Pixabay resolution, crops it to the selected canvas, trims, concatenates, overlays the audio track, and adjusts the total duration. The UI supports:

- **YouTube Short:** 1080×1920 (9:16 portrait)
- **Long Video:** 1280×720 (16:9 landscape)

The selected format is sent to the API as `video_format` and controls both Pixabay orientation and final rendering dimensions.

**Phase 2 (FFmpeg):** Burns the `.SRT` subtitle file into the video using FFmpeg's `subtitles` filter, producing the final hardcoded-subtitle MP4.

> ⚠️ **Real Bug Fixed:** Some Pixabay clips had no usable frames. Added clip validation before assembly — if too few clips, loops existing clips to fill duration.

---

### `youtube_service.py` — Step 8

Implements YouTube Data API v3 OAuth 2.0. On first run, opens a browser for authorization. Token saved locally for subsequent runs. Upload call sets: title, description, tags, category ID, privacy status (public).

---

### `pipeline_service.py` — The Orchestrator ★

The most architecturally important file. Calls all services in sequence. If any step fails, catches the exception and raises a clean `HTTPException` — the frontend always gets a meaningful error, never a raw traceback.

```python
def run_pipeline(niche: str):
    idea    = idea_service.generate(niche)
    script  = script_service.generate(idea)
    audio   = voice_service.generate(script)
    clips   = stock_video_service.fetch(idea["keywords"])
    subs    = subtitle_service.generate(script, audio)
    video   = video_service.render(clips, audio, subs)
    yt_url  = youtube_service.upload(video, idea)
    return {"video_path": video, "youtube_url": yt_url}
```

---

## 6. API Reference

### `POST /api/generate` — Main Pipeline Endpoint

**Request**
```json
{
  "niche": "fitness tips for beginners"
}
```

**Success Response** `200 OK`
```json
{
  "video_path": "artifacts/rendered_videos/abc123.mp4",
  "youtube_url": "https://youtube.com/watch?v=XYZ123abc"
}
```

**Error Response** `500 Internal Server Error`
```json
{
  "detail": "Pipeline failed at video rendering step."
}
```

| Property | Value |
|---|---|
| Handler | `app/api/routes/content.py` |
| Execution Chain | `content.py → pipeline_service → 8 services` |
| Auth Required | No (API keys are server-side in `.env`) |
| Processing Time | 3–8 minutes depending on API latency |

---

### `GET /` — Frontend

Serves `app/templates/index.html` via Jinja2. Returns the complete UI.

---

### YouTube OAuth Routes (`app/api/routes/youtube.py`)

Handles the OAuth 2.0 callback. The callback URL receives the authorization code, exchanges it for an access token, and stores it locally. Only needs to run once during initial setup.

---

## 7. Build From Scratch — Development Roadmap

### Phase 1: Planning (Before Writing Any Code)

- Define the full pipeline: idea → script → voice → footage → subtitles → video → upload
- Choose technology stack
- Sketch folder structure
- Sign up for all required APIs: Google AI Studio, Pixabay, YouTube/Google Cloud Console
- Decide on artifact storage: local disk in `artifacts/` folder

### Phase 2: Project Initialization

```bash
git init
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn google-generativeai kokoro-tts moviepy imageio-ffmpeg requests python-dotenv google-api-python-client google-auth-oauthlib pytest
pip freeze > requirements.txt
```

Create `.gitignore`:
```
.env
venv/
artifacts/
__pycache__/
*.pyc
.pytest_cache/
```

### Phase 3: Folder Structure & Configuration

```bash
mkdir -p app/api/routes app/core app/schemas app/services
mkdir -p app/templates app/static/css app/static/js app/utils
mkdir -p artifacts/audio artifacts/stock_videos artifacts/subtitles artifacts/rendered_videos
touch app/__init__.py app/api/__init__.py app/api/routes/__init__.py
touch app/core/__init__.py app/schemas/__init__.py app/services/__init__.py app/utils/__init__.py
```

> **Why first?** `config.py` and `logger.py` are imported by every other file. They must exist before anything else.

### Phase 4: Schemas & App Entry Point

- `app/schemas/request_schema.py` — Pydantic models for request/response
- `app/main.py` — FastAPI app, static files, routers, Jinja2 templates
- **Test:** `uvicorn app.main:app --reload` → server starts ✓

### Phase 5: Build Services (In Pipeline Order)

> Build and test each service individually before wiring them together.

```
5a → gemini_service.py    (confirms Gemini API key works)
5b → idea_service.py      (test: does Gemini return valid JSON?)
5c → script_service.py    (test: does the script read naturally?)
5d → voice_service.py     (test: is the MP3 file created?)
5e → stock_video_service.py (test: are clips downloaded?)
5f → subtitle_service.py  (test: is the .SRT file valid?)
5g → ffmpeg_utils.py + video_service.py (test: final MP4 renders?)
5h → youtube_service.py   (test: OAuth + test upload)
5i → pipeline_service.py  (wire all together, full end-to-end test)
```

### Phase 6: API Routes

- `app/api/routes/content.py` — define `POST /api/generate`
- `app/api/routes/youtube.py` — define OAuth callback
- Register both routers in `main.py`
- Test: `curl -X POST http://localhost:8000/api/generate -d '{"niche":"test"}'`

### Phase 7: Frontend

- `app/templates/index.html` — input form, progress section, result section
- `app/static/js/main.js` — `fetch()` call, progress display, video player, error handling
- `app/static/css/style.css` — visual styling
- **Test:** Full browser end-to-end run

### Phase 8: Testing

```bash
# Create test files
touch tests/test_gemini_service.py
touch tests/test_script_service.py
touch tests/test_pipeline.py

# Run all tests
pytest tests/ -v
```

### Phase 9: Deployment

```bash
# Install FFmpeg on server
sudo apt install ffmpeg

# Set environment variables in your hosting dashboard (not .env)

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Deployment options:** VPS (DigitalOcean, AWS EC2), PaaS (Railway, Render), Docker container.

---

## 8. File Dependency Map

```
app/main.py
  └── app/api/routes/content.py
        └── app/services/pipeline_service.py
              ├── app/services/idea_service.py
              │     └── app/services/gemini_service.py
              │           └── app/core/config.py
              ├── app/services/script_service.py
              │     └── app/services/gemini_service.py
              ├── app/services/voice_service.py
              │     └── app/core/config.py
              ├── app/services/stock_video_service.py
              │     └── app/core/config.py  (Pixabay API key)
              ├── app/services/subtitle_service.py
              ├── app/services/video_service.py
              │     └── app/utils/ffmpeg_utils.py
              ├── app/services/youtube_service.py
              │     └── app/core/config.py  (YouTube credentials)
              └── app/core/logger.py  (imported by all services)
```

### File Creation Order (When Building From Scratch)

| Step | File | Reason |
|---|---|---|
| 1 | `.env`, `.gitignore`, `requirements.txt` | Foundation — needed before anything |
| 2 | `app/core/config.py` | Loads env vars; every service imports this |
| 3 | `app/core/logger.py` | Logging; every service imports this |
| 4 | `app/schemas/request_schema.py` | Pydantic models for API validation |
| 5 | `app/services/gemini_service.py` | AI gateway; idea + script services depend on it |
| 6 | `app/services/idea_service.py` | Step 1 of pipeline |
| 7 | `app/services/script_service.py` | Needs idea output |
| 8 | `app/services/voice_service.py` | Needs script output |
| 9 | `app/services/stock_video_service.py` | Needs idea keywords |
| 10 | `app/services/subtitle_service.py` | Needs audio + script |
| 11 | `app/utils/ffmpeg_utils.py` | Helper for video_service |
| 12 | `app/services/video_service.py` | Needs clips + audio + subtitles |
| 13 | `app/services/youtube_service.py` | Needs final video |
| 14 | `app/services/pipeline_service.py` | Wires all services together |
| 15 | `app/api/routes/content.py` | Exposes pipeline to HTTP |
| 16 | `app/api/routes/youtube.py` | OAuth callback handling |
| 17 | `app/main.py` | Registers everything, starts app |
| 18 | `app/templates/index.html` | Frontend UI |
| 19 | `app/static/js/main.js` | Frontend logic |
| 20 | `app/static/css/style.css` | Frontend styling |
| 21 | `tests/` | Tests after all logic is working |

---

## 9. Configuration Files

### `.env` — Required Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
PIXABAY_API_KEY=your_pixabay_api_key_here
YOUTUBE_CLIENT_ID=your_oauth_client_id
YOUTUBE_CLIENT_SECRET=your_oauth_client_secret
YOUTUBE_REDIRECT_URI=http://localhost:8000/api/youtube/callback
```

> ⚠️ **Never commit `.env` to Git.** Add it to `.gitignore` immediately.

### `requirements.txt` — Key Packages

```
fastapi
uvicorn
google-generativeai
kokoro-tts
moviepy
imageio-ffmpeg
requests
python-dotenv
google-api-python-client
google-auth-oauthlib
pytest
```

### Getting API Keys

| API | Where to Get |
|---|---|
| Gemini API Key | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| Pixabay API Key | [Pixabay API](https://pixabay.com/api/docs/) |
| YouTube OAuth Credentials | [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials |

---

## 10. Security Analysis

### Current Measures ✅

- API keys stored in `.env`, never hardcoded in source
- `.env` in `.gitignore` — secrets never committed to GitHub
- Pydantic validation on all API inputs prevents malformed requests
- YouTube OAuth 2.0 — tokens stored locally, not transmitted
- All video processing runs server-side

### Production Security Gaps ⚠️

| Gap | Risk | Fix |
|---|---|---|
| No auth on `/api/generate` | Anyone can trigger pipeline (costs money) | Add API key auth or JWT tokens |
| No rate limiting | Server can be flooded with requests | Add `slowapi` (e.g. 3 req/hour/IP) |
| No input sanitization on niche field | Potential injection | Validate max length, strip special chars |
| Artifacts folder publicly accessible | Users can access others' videos | Move to private storage + signed URLs |

---

## 11. Scalability & Future Improvements

### Current Limitations

- Pipeline runs synchronously — one video at a time per server process
- Artifacts stored on local disk — breaks on multi-server deployments
- No job queue — concurrent requests block each other
- No caching — same niche hits the AI API every time

### Planned Improvements

| Enhancement | Description |
|---|---|
| **Background Task Queue** | Celery + Redis — return job ID immediately, poll for status |
| **WebSocket Progress** | Real-time step-by-step progress instead of waiting for completion |
| **Cloud Storage** | AWS S3 or Google Cloud Storage for artifacts |
| **Database** | PostgreSQL for video history, user accounts, analytics |
| **Caching** | Redis cache for identical niche Gemini responses |
| **Docker** | Containerize for consistent environments across deployments |
| **User Authentication** | Multi-user support with per-user YouTube channels |
| **Video Scheduling** | Queue videos for future upload times |
| **Thumbnail Generation** | AI-generated custom thumbnails |
| **Multi-language Support** | Generate scripts and voiceovers in multiple languages |
| **Analytics Dashboard** | Track video performance across the channel |

---

## 12. Challenges & Solutions

| Challenge | What Happened | Solution & Lesson |
|---|---|---|
| **Gemini Model Migration** | Google deprecated the original model mid-project | Because all AI calls were centralized in `gemini_service.py`, only one file needed updating. **Lesson:** Always abstract external APIs. |
| **FFmpeg Subtitle Rendering** | MoviePy couldn't reliably burn subtitles | Used FFmpeg directly via subprocess for subtitle burning, kept MoviePy for clip assembly. **Lesson:** Use the right tool for each job. |
| **Empty Video Clips** | Some Pixabay results were corrupt or had no frames | Added clip validation in `stock_video_service.py` before passing to `video_service.py`. **Lesson:** Never trust external API responses. |
| **YouTube OAuth Setup** | OAuth redirect URI must exactly match Google Console registration | Documented setup steps clearly. Common source of confusion for new developers. |
| **Python Version Compatibility** | Kokoro TTS required specific Python version | Locked Python to 3.11 in documentation and CI/CD. |
| **Frontend-Backend Sync** | Frontend needed to know when pipeline completed | Pipeline blocks synchronously and returns full result. Works for MVP — replace with WebSockets for production. |

---

## 13. Quick Start

### Prerequisites

- Python 3.11
- Git
- API keys for: Gemini, Pixabay, YouTube (see [Configuration Files](#9-configuration-files))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/098devendrasharma/Youtube_AI_Automation
cd Youtube_AI_Automation

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Open .env and fill in your API keys

# 5. Run the application
uvicorn app.main:app --reload

# 6. Open browser
# Visit: http://localhost:8000
```

### First-Time YouTube Setup

On the first run, the YouTube OAuth flow will open a browser window asking you to authorize the app with your Google account. After authorization, the token is saved locally and subsequent runs will not require re-authorization.

### Usage

1. Open `http://localhost:8000` in your browser
2. Enter a content niche (e.g. `"5 morning habits of successful people"`)
3. Click **Generate**
4. Watch each pipeline step complete with progress indicators
5. When done: the final video plays in the browser and the YouTube link is displayed

---

## 14. Final Summary

### How It Works (30-Second Version)

1. You type a niche → FastAPI receives it at `POST /api/generate`
2. `pipeline_service.py` orchestrates 8 services in sequence
3. Gemini AI generates the idea + script
4. Kokoro TTS converts script to audio
5. Pixabay provides stock footage
6. MoviePy + FFmpeg assemble and render the final video
7. YouTube API uploads it
8. You get a video URL back in your browser

### The 5 Most Important Files

| File | Why It Matters |
|---|---|
| `pipeline_service.py` | The brain — orchestrates everything |
| `gemini_service.py` | All intelligence flows through here |
| `video_service.py` | The hardest file — MoviePy + FFmpeg |
| `main.py` | The entry point — starts the whole app |
| `config.py` | The foundation — every file depends on it |

### Key Architectural Principles

- **Single Responsibility** — each service does exactly one job
- **Adapter Pattern** — `gemini_service.py` wraps Gemini behind your own interface
- **Pipeline Pattern** — sequential transformation of data through discrete stages
- **Configuration Externalization** — no hardcoded secrets; all keys in `.env`
- **Error Containment** — `pipeline_service` catches and wraps all errors before the API layer

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

---

*End-to-end AI automation in real-world media production.*
