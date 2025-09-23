from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "appdb"
    COLLECTION_NAME: str = "items"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", env_file_encoding="utf-8")

settings = Settings()