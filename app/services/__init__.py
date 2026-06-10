from app.services.youtube_service import (
    YouTubeService
)

class PipelineService:

    def __init__(self):

        self.youtube_service = (
            YouTubeService()
        )