# app/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    NVIDIA_API_KEY: str
    DATABASE_URL: str = "chroma_data"
    
    # Use simple approach - we'll skip NVIDIA embeddings for now
    MODEL_EMBEDDING: str = "simple"  # Don't use NVIDIA for embeddings initially
    MODEL_REASONING: str = "meta/llama-3.1-8b-instruct"
    
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()