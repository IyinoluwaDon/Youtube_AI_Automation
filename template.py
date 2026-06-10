import os
from pathlib import Path

PROJECT_NAME = "."

list_of_files = [

    # Root Files
    f"README.md",
    f"requirements.txt",
    f"setup.py",
    f"pyproject.toml",
    f".gitignore",
    f".env",

    # Application
    f"app/__init__.py",
    f"app/main.py",

    # API
    f"app/api/__init__.py",
    f"app/api/dependencies.py",

    f"app/api/routes/__init__.py",
    f"app/api/routes/content.py",
    f"app/api/routes/video.py",
    f"app/api/routes/upload.py",
    f"app/api/routes/youtube.py",

    # Core
    f"app/core/__init__.py",
    f"app/core/config.py",
    f"app/core/constants.py",
    f"app/core/logger.py",
    f"app/core/security.py",

    # Services
    f"app/services/__init__.py",
    f"app/services/gemini_service.py",
    f"app/services/script_service.py",
    f"app/services/voice_service.py",
    f"app/services/subtitle_service.py",
    f"app/services/stock_video_service.py",
    f"app/services/video_service.py",
    f"app/services/youtube_service.py",

    # Schemas
    f"app/schemas/__init__.py",
    f"app/schemas/request_schema.py",
    f"app/schemas/response_schema.py",

    # Models
    f"app/models/__init__.py",
    f"app/models/job_model.py",

    # Utils
    f"app/utils/__init__.py",
    f"app/utils/exception.py",
    f"app/utils/helpers.py",
    f"app/utils/ffmpeg_utils.py",
    f"app/utils/file_manager.py",

    # Templates
    f"app/templates/index.html",
    f"app/templates/status.html",
    f"app/templates/result.html",

    # Static
    f"app/static/css/style.css",
    f"app/static/js/app.js",

    # Artifacts
    f"artifacts/scripts/.gitkeep",
    f"artifacts/audio/.gitkeep",
    f"artifacts/subtitles/.gitkeep",
    f"artifacts/stock_videos/.gitkeep",
    f"artifacts/rendered_videos/.gitkeep",
    f"artifacts/thumbnails/.gitkeep",

    # Logs
    f"logs/application.log",

    # Tests
    f"tests/__init__.py",
    f"tests/test_api.py",
    f"tests/test_gemini.py",
    f"tests/test_video.py",

    # GitHub Actions
    f".github/workflows/ci.yml",
    f".github/workflows/cd.yml",
]

for filepath in list_of_files:

    filepath = Path(filepath)

    filedir = filepath.parent

    filedir.mkdir(parents=True, exist_ok=True)

    if not filepath.exists():
        filepath.touch()

print("Project Structure Created Successfully")