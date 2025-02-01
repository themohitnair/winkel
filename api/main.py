from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.initialize import Database
from config import setup_logging
import logging
from routes import member, listing, category, parameter, media, metric

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database()
    logger = logging.getLogger(__name__)

    try:
        await db.connect()

        async with db.pool.acquire() as connection:
            if not await db.db_exists(connection):
                await db.create_db(connection)

            await db.create_tables(connection)

            await db.seed_categories(connection)

        app.state.db = db

        yield
    except Exception as e:
        logger.critical("Error during database setup: %s", e, exc_info=True)
        raise
    finally:
        if hasattr(app.state, "db"):
            await app.state.db.disconnect()
            logger.info("Database disconnected")


app = FastAPI(lifespan=lifespan)

app.include_router(member.router)
app.include_router(listing.router)
app.include_router(category.router)
app.include_router(media.router)
app.include_router(metric.router)
app.include_router(parameter.router)


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
