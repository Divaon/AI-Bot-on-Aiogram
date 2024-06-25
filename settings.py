from aiogram import Bot
from openai import OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict

# some settings
class Settings(BaseSettings):
    TOKEN_API: str
    TOKEN_OPENAI: str
    ASSISTANT_ID: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()


bot = Bot(token=config.TOKEN_API)
client = OpenAI(
    api_key=config.TOKEN_OPENAI,
)
