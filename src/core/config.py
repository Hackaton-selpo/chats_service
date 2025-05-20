from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE", env_file=".env")
    database_host: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str


db_config = DBConfig()
