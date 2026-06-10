from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.request_schema import (
    YoutubeUploadRequest
)

from app.services.youtube_service import (
    YouTubeService
)

router = APIRouter()

youtube_service = YouTubeService()


@router.post("/upload")

def upload_video(
    request: YoutubeUploadRequest
):

    try:

        response = (
            youtube_service.upload_video(
                video_path=request.video_path,
                title=request.title,
                description=request.description
            )
        )

        return {

            "status": "success",

            "youtube_video_id":
                response["id"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )