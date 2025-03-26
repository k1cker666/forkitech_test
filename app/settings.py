from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_prefix="psql_", env_file_encoding="utf-8", extra="ignore",
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

class TronGrid(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_prefix="trongrid_", env_file_encoding="utf-8", extra="ignore",
    )
    api_key: str

class Settings(BaseSettings):
    postgresql: PostgreSQLSettings = PostgreSQLSettings()
    trongrid: TronGrid = TronGrid()


settings = Settings()
