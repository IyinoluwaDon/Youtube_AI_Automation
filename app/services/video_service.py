from pathlib import Path

from moviepy import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips
)

from app.core.logger import logger


class VideoService:

    def create_video(
        self,
        video_files: list,
        audio_file: str,
        output_file: str
    ):

        logger.info(
            "Starting Video Rendering"
        )

        if not video_files:

            raise ValueError(
                "No video files found."
            )

        audio = AudioFileClip(
            audio_file
        )

        target_duration = (
            audio.duration
        )

        clips = []

        total_video_duration = 0

        while (
            total_video_duration
            < target_duration
        ):

            for file in video_files:

                clip = VideoFileClip(
                    str(file)
                )

                clips.append(
                    clip
                )

                total_video_duration += (
                    clip.duration
                )

                if (
                    total_video_duration
                    >= target_duration
                ):
                    break

        final_video = (
            concatenate_videoclips(
                clips,
                method="compose"
            )
            .subclipped(
                0,
                target_duration
            )
        )

        final_video = (
            final_video
            .with_audio(audio)
        )

        final_video.write_videofile(
            output_file,
            codec="libx264",
            audio_codec="aac",
            fps=30,
            threads=4
        )

        logger.info(
            f"Video Saved -> {output_file}"
        )

        return Path(output_file)