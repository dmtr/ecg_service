import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ecg_service.config import app_configs, settings
from ecg_service.database import get_database
from ecg_service.user.repository import UserRepository

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()
    logger.info("Creating indexes")
    await db.user.create_index("email", unique=True)

    if settings.ENVIRONMENT == "LOCAL":
        logger.info("Creating admin user")
        user_repository = UserRepository(db)
        if not await user_repository.get_user_by_email(email=settings.ADMIN_USER):
            await user_repository.create_admin(
                email=settings.ADMIN_USER, password=settings.ADMIN_PASSWORD
            )

    yield


app = FastAPI(**app_configs, lifespan=lifespan)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    db = get_database()
    await db.command("ping")
    return {"status": "ok"}
