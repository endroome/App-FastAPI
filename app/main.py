from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from contextlib import asynccontextmanager

from .endpoints import router
from .settings import settings
from .database import engine
from .models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key_header


app.include_router(router, prefix="/api/v1", dependencies=[Depends(get_api_key)])
