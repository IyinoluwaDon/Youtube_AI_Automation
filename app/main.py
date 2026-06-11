from pathlib import Path

from fastapi import FastAPI
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes.content import (
    router as content_router
)

from app.api.routes.youtube import (
    router as youtube_router
)

# --------------------------------------------------
# Ensure required directories exist
# --------------------------------------------------

Path("artifacts").mkdir(
    exist_ok=True
)

Path(
    "artifacts/rendered_videos"
).mkdir(
    parents=True,
    exist_ok=True
)

Path(
    "artifacts/audio"
).mkdir(
    parents=True,
    exist_ok=True
)

Path(
    "artifacts/subtitles"
).mkdir(
    parents=True,
    exist_ok=True
)

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(

    title=
    "YouTube AI Automation",

    description=
    "AI-powered YouTube Shorts Automation Platform",

    version=
    "1.0.0"
)

# --------------------------------------------------
# Static Files
# --------------------------------------------------

app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static"
)

# --------------------------------------------------
# Generated Files
# --------------------------------------------------

app.mount(

    "/artifacts",

    StaticFiles(
        directory="artifacts"
    ),

    name="artifacts"
)

# --------------------------------------------------
# Templates
# --------------------------------------------------

templates = Jinja2Templates(

    directory=
    "app/templates"
)

# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(

    content_router,

    prefix=
    "/api/content",

    tags=[
        "Content"
    ]
)

app.include_router(

    youtube_router,

    prefix=
    "/api/youtube",

    tags=[
        "YouTube"
    ]
)

# --------------------------------------------------
# Home Page
# --------------------------------------------------
@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get(
    "/health"
)
async def health():

    return {

        "status":
        "healthy",

        "application":
        "YouTube AI Automation"
    }