from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    PROJECT_NAME: str = "TintTQ AI"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str
    SYNC_DB_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Storage
    UPLOAD_DIR: str = "app/uploads"
    GENERATED_DIR: str = "app/generated"

    # AI Settings
    YOLO_MODEL_PATH: str = "models/yolov8/tint_detector.pt"

    # class Config:
    #     env_file = ".env"
    #     extra = "ignore"


settings = Settings()