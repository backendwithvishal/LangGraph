import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "GraphLab API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    EXECUTION_TIMEOUT_SECONDS: int = 15
    MAX_OUTPUT_BYTES: int = 100000

settings = Settings()
