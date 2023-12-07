from fastapi import FastAPI

from ecg_service.config import app_configs

app = FastAPI(**app_configs)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
