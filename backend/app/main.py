import asyncio
import anyio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from app.core.config import settings
from app.core.database import Base, engine
from app.core.middleware import LoggingMiddleware
from app.routers import pais as pais_router

async def init_db():
    # Helper to run blocking create_all in a thread
    try:
        await anyio.to_thread.run_sync(Base.metadata.create_all, engine)
    except Exception:
        # DB might be offline, that's okay for startup
        pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Launch DB init as a background task so it doesn't block startup
    asyncio.create_task(init_db())
    yield
    # Shutdown logic if needed
    # Shutdown logic if needed

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pais_router.router, prefix="/api/v1")


@app.get("/health")
def health():
    db_status = "ok"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
    return {
        "status": "ok",
        "db_status": db_status,
        "version": settings.app_version
    }
