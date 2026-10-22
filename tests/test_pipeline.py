"""Manual integration exercise; may call external providers when run directly."""
if __name__ == "__main__":
    from app.services.pipeline_service import (
        PipelineService
    )

    pipeline = PipelineService()

    result = pipeline.run(
        niche="Artificial Intelligence"
    )

    print(result)
