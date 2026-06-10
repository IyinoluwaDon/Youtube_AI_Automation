from app.services.pipeline_service import (
    PipelineService
)

pipeline = PipelineService()

result = pipeline.run(
    niche="Artificial Intelligence"
)

print(result)