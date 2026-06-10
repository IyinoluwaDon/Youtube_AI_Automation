import json
import time

from google import genai
from google.genai import types

from app.core.config import settings
from app.core.logger import logger


class GeminiService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate_content(
        self,
        prompt: str,
        system: str = "",
        max_retries: int = 3
    ):
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system if system else None
                    )
                )
                return response.text

            except Exception as e:
                logger.error(f"Gemini Error: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)

    def generate_json(
        self,
        prompt: str,
        system: str = "",
        max_retries: int = 3
    ):
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system if system else None,
                        response_mime_type="application/json"
                    )
                )
                return json.loads(response.text)

            except Exception as e:
                logger.error(f"Gemini JSON Error: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)