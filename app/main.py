from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes.content import router as content_router
from app.api.routes.youtube import router as youtube_router

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)

# Register routers
app.include_router(
    content_router,
    prefix="/api/content"
)

app.include_router(
    youtube_router,
    prefix="/api/youtube"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
