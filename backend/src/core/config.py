from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_CONN_STR: str
    JWT_SECRET_KEY: str

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()