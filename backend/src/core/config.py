from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ці два поля обов'язкові і мають бути в .env
    DATABASE_CONN_STR: str
    JWT_SECRET_KEY: str
    
    # А цим ми даємо значення за замовчуванням, щоб не було помилок
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()