from pydantic import BaseModel
import os

class Settings(BaseModel):
    provider: str = os.getenv("PROVIDER", "openai").lower()
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "60"))

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    azure_api_key: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str | None = os.getenv("OPENROUTER_MODEL")

    chroma_path: str = os.getenv("CHROMA_PATH", "./chroma")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

settings = Settings()
