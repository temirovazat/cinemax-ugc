from functools import lru_cache

from pydantic import BaseModel, BaseSettings, Field


class MongoConfig(BaseModel):
    """Configuration class for MongoDB connection settings."""

    host: str = 'localhost'
    port: int = 27017
    db: str = 'default'


class LogstashConfig(BaseModel):
    """Configuration class for Logstash connection settings."""

    host: str = 'localhost'
    port: int = 5044


class SentryConfig(BaseModel):
    """Configuration class for Sentry connection settings."""

    dsn: str = ''


class FastApiConfig(BaseModel):
    """Configuration class for FastAPI settings."""

    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = False
    docs: str = 'openapi'
    secret_key: str = 'secret_key'
    title: str = 'API for monitoring user-generated content'


class MainSettings(BaseSettings):
    """Main project settings class."""

    fastapi: FastApiConfig = Field(default_factory=FastApiConfig)
    mongo: MongoConfig = Field(default_factory=MongoConfig)
    sentry: SentryConfig = Field(default_factory=SentryConfig)
    logstash: LogstashConfig = Field(default_factory=LogstashConfig)


@lru_cache()
def get_settings():
    """Create a singleton settings object.

    Returns:
        MainSettings: Settings object.
    """
    return MainSettings(_env_file='.env', _env_nested_delimiter='_')


CONFIG = get_settings()
