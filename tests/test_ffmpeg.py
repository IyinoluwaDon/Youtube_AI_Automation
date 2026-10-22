"""Manual integration exercise; may call external providers when run directly."""
if __name__ == "__main__":
    # tests/test_ffmpeg.py

    import imageio_ffmpeg

    print(
        imageio_ffmpeg.get_ffmpeg_exe()
    )

    from app.utils.ffmpeg_utils import burn_subtitles

    burn_subtitles(
        "artifacts/rendered_videos/raw.mp4",
        "artifacts/subtitles/output.srt",
        "artifacts/rendered_videos/final.mp4"
    )
