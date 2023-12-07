from enum import Enum
from typing import Any

from pydantic import MongoDsn
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_production(self) -> bool:
        return self in (self.PRODUCTION,)


class Config(BaseSettings):
    MONGODB_URL: MongoDsn
    SITE_DOMAIN: str = "myapp.com"
    ENVIRONMENT: Environment = Environment.LOCAL
    SECRET_KEY: str


settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}

if settings.ENVIRONMENT.is_debug:
    app_configs["debug"] = True
else:
    app_configs["openapi_url"] = None
