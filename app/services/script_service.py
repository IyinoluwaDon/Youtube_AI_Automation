import json

from app.services.gemini_service import GeminiService
from app.core.logger import logger


class ScriptService:

    def __init__(self):

        self.gemini = GeminiService()

    def generate_script(
        self,
        idea: dict
    ) -> dict:

        system = (
            "You are a professional short-form "
            "video scriptwriter. "
            "Return ONLY valid JSON."
        )

        prompt = f"""
Write a narration script for this short-form video idea:

{json.dumps(idea, indent=2)}

Return a JSON object with EXACTLY these keys:

{{
  "script":"<full narration>",
  "duration_estimate":60,
  "segments":[
    {{
      "label":"hook",
      "text":""
    }},
    {{
      "label":"point_1",
      "text":""
    }},
    {{
      "label":"point_2",
      "text":""
    }},
    {{
      "label":"point_3",
      "text":""
    }},
    {{
      "label":"cta",
      "text":""
    }}
  ]
}}

Rules:

- Total words 150-225
- Conversational tone
- No markdown
- No stage directions
- No parenthetical notes
"""

        result = self.gemini.generate_json(
            prompt=prompt,
            system=system
        )

        logger.info(
            "Script generated successfully"
        )

        return result