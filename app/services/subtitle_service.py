from pathlib import Path

from app.core.logger import logger


class SubtitleService:

    def __init__(self):
        pass

    def generate_srt(
        self,
        script_data: dict,
        total_duration: float,
        output_file: str
    ) -> Path:

        segments = script_data["segments"]

        all_words = []

        for segment in segments:

            words = (
                segment["text"]
                .split()
            )

            all_words.extend(words)

        total_words = len(all_words)

        if total_words == 0:

            raise ValueError(
                "No words found in script."
            )

        word_duration = (
            total_duration
            / total_words
        )

        chunk_size = 3

        subtitles = []

        subtitle_index = 1

        current_time = 0.0

        def format_time(seconds):

            hours = int(
                seconds // 3600
            )

            minutes = int(
                (seconds % 3600) // 60
            )

            secs = int(
                seconds % 60
            )

            milliseconds = int(
                (
                    seconds
                    - int(seconds)
                ) * 1000
            )

            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{secs:02d},"
                f"{milliseconds:03d}"
            )

        for i in range(
            0,
            total_words,
            chunk_size
        ):

            chunk = all_words[
                i:i + chunk_size
            ]

            text = " ".join(chunk)

            start_time = (
                current_time
            )

            end_time = (
                current_time
                + (
                    len(chunk)
                    * word_duration
                )
            )

            subtitles.append(
                f"{subtitle_index}\n"
                f"{format_time(start_time)} --> "
                f"{format_time(end_time)}\n"
                f"{text}\n"
            )

            subtitle_index += 1

            current_time = end_time

        output_path = Path(
            output_file
        )

        output_path.write_text(
            "\n".join(subtitles),
            encoding="utf-8"
        )

        logger.info(
            f"SRT Saved -> {output_path}"
        )

        return output_path