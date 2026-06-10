from app.core.config import settings

from app.services.idea_service import IdeaService
from app.services.script_service import ScriptService

print("API Key Loaded:", bool(settings.GEMINI_API_KEY))

try:

    idea_service = IdeaService()

    idea = idea_service.generate_video_idea(
        niche="Artificial Intelligence"
    )

    print("\nIDEA\n")
    print(idea)

    script_service = ScriptService()

    script = script_service.generate_script(
        idea
    )

    print("\nSCRIPT\n")
    print(script)

except Exception as e:

    print("\nERROR\n")
    print(str(e))