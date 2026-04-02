from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# configuration class to manage environment variables
class Config(BaseSettings):
    openai_api_key: str
    pushover_user: str
    pushover_token: str
    pushover_url:str = "https://api.pushover.net/1/messages.json"
    model_name: str = "gpt-4o"
    prompt_file: str = "src/prompts/prompts.yaml"
    user: str = 'Abhisek Behera'
    user_role: str = 'Lead AI and Data Engineer'
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')

# function to get configuration with caching
@lru_cache()
def get_config():
    return Config()

settings = get_config()