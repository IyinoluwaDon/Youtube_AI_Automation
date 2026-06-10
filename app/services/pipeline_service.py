from app.services.idea_service import (
    IdeaService
)

from app.services.script_service import (
    ScriptService
)

from app.services.voice_service import (
    VoiceService
)

from app.services.stock_video_service import (
    StockVideoService
)

from app.services.subtitle_service import (
    SubtitleService
)

from app.services.video_service import (
    VideoService
)

from app.services.youtube_service import (
    YouTubeService
)

from app.utils.ffmpeg_utils import (
    burn_subtitles
)

from app.utils.helpers import (
    ensure_artifact_folders
)


class PipelineService:

    def __init__(self):

        self.idea_service = IdeaService()

        self.script_service = ScriptService()

        self.voice_service = VoiceService()

        self.stock_service = (
            StockVideoService()
        )

        self.subtitle_service = (
            SubtitleService()
        )

        self.video_service = (
            VideoService()
        )

        self.youtube_service = (
            YouTubeService()
        )

    def run(
        self,
        niche
    ):

        ensure_artifact_folders()

        # Generate Idea
        idea = (
            self.idea_service
            .generate_video_idea(
                niche
            )
        )

        # Generate Script
        script = (
            self.script_service
            .generate_script(
                idea
            )
        )

        # Generate Voice
        audio = (
            self.voice_service
            .generate_voiceover(
                script,
                "artifacts/audio/output.wav"
            )
        )

        # Download Stock Videos
        clips = (
            self.stock_service
            .download_clips(
                idea["keywords"]
            )
        )

        print("\n========== CLIPS ==========")
        print(clips)
        print("COUNT:", len(clips))
        print("===========================\n")

        if not clips:

            raise ValueError(
                """
No stock videos downloaded.

Check:
1. PEXELS_API_KEY
2. Internet Connection
3. Pexels API Response
                """
            )

        # Generate Subtitles
        subtitle = (
            self.subtitle_service
            .generate_srt(
                script,
                script["duration_estimate"],
                "artifacts/subtitles/output.srt"
            )
        )

        # Render Video
        raw_video = (
            self.video_service
            .create_video(
                clips,
                audio,
                "artifacts/rendered_videos/raw.mp4"
            )
        )

        # Burn Subtitles
        final_video = burn_subtitles(
            str(raw_video),
            str(subtitle),
            "artifacts/rendered_videos/final.mp4"
        )

        # Upload To YouTube
        youtube_video = (
            self.youtube_service
            .upload_video(
                str(final_video),
                idea["title"],
                script["script"]
            )
        )

        return {

            "idea": idea,

            "script": script,

            "video": str(final_video),

            "youtube_id":
            youtube_video["id"],

            "youtube_url":
            youtube_video["url"]
        }