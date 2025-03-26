from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_prefix="psql_", env_file_encoding="utf-8"
    )
    dbname: str
    user: str
    password: str
    host: str
    port: str

    def get_conninfo(self):
        conninfo = (
            f"postgresql+asyncpg://{self.user}:"
            + f"{self.password}@{self.host}:{self.port}/{self.dbname}"
        )
        return conninfo

class Settings(BaseSettings):
    postgresql: PostgreSQLSettings = PostgreSQLSettings()


settings = Settings()
