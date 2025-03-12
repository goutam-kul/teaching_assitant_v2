from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    text_model: str = "mistral:latest"
    image_model: str = "llava:latest"


def get_settings() -> Settings:
    """Get base settings"""
    return Settings()