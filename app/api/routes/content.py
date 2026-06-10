import asyncio

from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.request_schema import (
    VideoGenerationRequest
)

from app.services.pipeline_service import (
    PipelineService
)

router = APIRouter()

pipeline = PipelineService()


@router.post("/generate")
async def generate_video(
    request: VideoGenerationRequest
):

    try:

        loop = asyncio.get_event_loop()

        result = await loop.run_in_executor(
            None,
            pipeline.run,
            request.niche
        )

        return {

            "status": "success",

            "niche": request.niche,

            "title": result["idea"]["title"],

            "video_path": result["video"],

            "youtube_id": result["youtube_id"],

            "youtube_url": result["youtube_url"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
