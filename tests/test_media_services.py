"""Manual integration exercise; may call external providers when run directly."""
if __name__ == "__main__":
    from app.services.voice_service import VoiceService
    from app.services.subtitle_service import SubtitleService

    script_data = {
        "duration_estimate": 60,
        "segments": [
            {
                "label": "hook",
                "text": "Artificial Intelligence is changing everything."
            },
            {
                "label": "point",
                "text": "Developers are automating work faster than ever."
            }
        ]
    }

    tts = VoiceService()

    audio = tts.generate_voiceover(
        script_data,
        "artifacts/audio/test.wav"
    )

    print(audio)

    subtitle = SubtitleService()

    srt = subtitle.generate_srt(
        script_data,
        60,
        "artifacts/subtitles/test.srt"
    )

    print(srt)
