from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    embedding_model: str
    vector_db: str
    max_concurrent_tasks: int
    rate_limit: int

    class Config:
        env_file = ".env"

settings = Settings()
