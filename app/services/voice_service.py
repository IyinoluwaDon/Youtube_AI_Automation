from pathlib import Path

import numpy as np
import soundfile as sf

from kokoro import KPipeline

from app.core.config import settings
from app.core.logger import logger


class VoiceService:

    def __init__(self):

        self.voice = "af_heart"

        self.pipeline = KPipeline(
            lang_code="a"
        )

    def generate_voiceover(
        self,
        script_data: dict,
        output_file: str
    ) -> Path:

        full_text = " ".join(
            seg["text"]
            for seg in script_data["segments"]
        )

        audio_chunks = []

        logger.info(
            f"Generating voice using {self.voice}"
        )

        for _, _, audio in self.pipeline(
            full_text,
            voice=self.voice,
            speed=1.0,
            split_pattern=r"\n+"
        ):
            audio_chunks.append(audio)

        combined_audio = np.concatenate(
            audio_chunks
        )

        output_path = Path(output_file)

        sf.write(
            str(output_path),
            combined_audio,
            samplerate=24000
        )

        logger.info(
            f"Voice saved -> {output_path}"
        )

        return output_path