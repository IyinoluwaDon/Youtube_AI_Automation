from pydantic import BaseModel, Field


class VideoGenerationRequest(BaseModel):

    niche: str = Field(
        ...,
        min_length=3,
        max_length=100
    )


class YoutubeUploadRequest(BaseModel):

    video_path: str

    title: str

    description: str