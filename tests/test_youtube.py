"""Manual integration exercise; may call external providers when run directly."""
if __name__ == "__main__":
    from app.services.youtube_service import (
        YouTubeService
    )

    youtube = YouTubeService()

    result = youtube.upload_video(
        video_path="artifacts/rendered_videos/final.mp4",
        title="Test Upload",
        description="Testing YouTube Upload"
    )

    print(result)
