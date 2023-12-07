import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ecg_service.config import app_configs
from ecg_service.database import get_database

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()
    logger.info("Creating indexes")
    await db.user.create_index("email", unique=True)
    yield


app = FastAPI(**app_configs, lifespan=lifespan)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    db = get_database()
    await db.command("ping")
    return {"status": "ok"}
