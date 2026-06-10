from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GEMINI_API_KEY: str

    PEXELS_API_KEY: str

    PIXABAY_API_KEY: str

    YOUTUBE_CLIENT_SECRET_FILE: str

    OUTPUT_DIR: str = "artifacts"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()