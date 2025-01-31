from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.initialize import Database
from config import setup_logging
import logging
from routes import user

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger(__name__)
    try:
        async with Database() as db:
            logger.info("Database initialized")
            yield
    except Exception as e:
        logger.critical("Database initialization failed: %s", e, exc_info=True)


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)


@app.get("/")
async def greet():
    logger = logging.getLogger(__name__)
    logger.info("Greeting endpoint accessed")
    return {"message": "Hello from winkel!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        port=8000, host="localhost", app="main:app", reload=True, log_config=None
    )
