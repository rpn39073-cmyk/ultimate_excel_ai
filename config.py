import os

class Settings:
    PROJECT_NAME: str = "Ultimate Excel AI Analyst"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey123")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    UPLOAD_DIR: str = os.path.join(os.getcwd(), "uploads")
    
    # ML Settings
    MODEL_TIMEOUT: int = 300 # seconds
    
    class Config:
        case_sensitive = True

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
