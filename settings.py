from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    TOKEN_API: str
    TOKEN_OPANAI: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()