from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra='ignore'
) 

class ApiConfig(BaseSettings):
    model_config = _base_config
    
    environment: str = Field(default="development")
    database_url: str = Field(default="*")
    test_database_url: str = Field(default="*")
    echo_sql: bool = True 

config = ApiConfig()

print(config)