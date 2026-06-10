from pydantic import BaseModel


class VideoGenerationResponse(BaseModel):

    status: str

    niche: str

    video_path: str

    title: str


class YoutubeUploadResponse(BaseModel):

    status: str

    youtube_video_id: str