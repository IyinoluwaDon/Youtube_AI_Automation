import json

from app.services.gemini_service import GeminiService
from app.core.logger import logger


class IdeaService:

    def __init__(self):

        self.gemini = GeminiService()

    def generate_video_idea(
        self,
        niche: str
    ) -> dict:

        system = """
You are an expert viral YouTube Shorts strategist.

Return ONLY valid JSON.
No markdown.
No explanation.
"""

        prompt = f"""
Generate one viral YouTube Shorts idea.

NICHE:
{niche}

Return JSON:

{{
    "title":"",
    "hook":"",
    "target_audience":"",
    "keywords":[],
    "video_style":"",
    "estimated_duration":60
}}
"""

        result = self.gemini.generate_json(
            prompt=prompt,
            system=system
        )

        logger.info(
            f"Idea Generated: {result['title']}"
        )

        return result