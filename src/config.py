from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = Field(default="local", alias="APP_ENV")

    kafka_bootstrap_servers: str = Field(default="localhost:19092", alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic: str = Field(default="transactions", alias="KAFKA_TOPIC")
    kafka_group_id: str = Field(default="fraud-detector", alias="KAFKA_GROUP_ID")

    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="frauddb", alias="POSTGRES_DB")
    postgres_user: str = Field(default="fraud", alias="POSTGRES_USER")
    postgres_password: str = Field(default="fraud", alias="POSTGRES_PASSWORD")

    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    fraud_alert_threshold: float = Field(default=0.72, alias="FRAUD_ALERT_THRESHOLD")
    producer_sleep_seconds: float = Field(default=0.5, alias="PRODUCER_SLEEP_SECONDS")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()

