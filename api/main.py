from config import LOG_CONFIG

from routers.field import field_router
from routers.listing import listing_router
from routers.media import media_router
from routers.user import user_router

# from config import TURSO_AUTH, TURSO_URL

from database import Database

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

import logging.config

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("🚀 FastAPI is starting up...")

        # db = Database(url=TURSO_URL, auth_token=TURSO_AUTH)

        db = Database(url="file:local.db")
        await db.create_tables()

        yield

    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)

    finally:
        try:
            logger.info("FastAPI is shutting down...")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}", exc_info=True)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(field_router, prefix="/fields", tags=["Fields"])
app.include_router(listing_router, prefix="/listings", tags=["Listings"])
app.include_router(media_router, prefix="/media", tags=["Media"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
async def greet():
    return {"message": "winkel says hello!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
