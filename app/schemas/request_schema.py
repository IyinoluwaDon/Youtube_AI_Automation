from typing import Literal

from pydantic import BaseModel, Field


class VideoGenerationRequest(BaseModel):

    niche: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    video_format: Literal["short", "long"] = "short"


class YoutubeUploadRequest(BaseModel):

    video_path: str

    title: str

    description: str