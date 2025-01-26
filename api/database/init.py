import aiosqlite
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = "database.db"):
        self.db_path: str = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_path)

        await self.conn.execute("PRAGMA foreign_keys = ON")
        await self.conn.commit()
        logger.info("Database connection established. ")

    async def close(self):
        if self.conn:
            await self.conn.close()
            logger.info("Database connection closed. ")

    async def seed_categories(self):
        categories = [
            ("Books",),
            ("Electronics",),
            ("Furniture",),
            ("Stationery",),
            ("Clothing",),
            ("Accessories",),
            ("Sports Equipment",),
            ("Musical Instruments",),
            ("Vehicles",),
            ("Room Decor",),
            ("Kitchenware",),
            ("Health & Fitness",),
            ("Gaming",),
            ("Miscellaneous",),
        ]
        await self.conn.executemany(
            "INSERT OR IGNORE INTO category (category_name) VALUES (?)", categories
        )
        await self.conn.commit()

    async def init_db(self):
        if not self.conn:
            await self.connect()

        if not self.conn:
            raise ConnectionError("Could not connect to the database. ")

        await self.conn.execute("BEGIN")
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                uni_serial_number TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                ph_no TEXT NOT NULL,
                rating REAL NOT NULL DEFAULT 0.0,
            );
            """
        )

        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """
        )

        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS listing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_name TEXT NOT NULL,
                listing_price REAL NOT NULL,
                category_id INTEGER,
                desc TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            """
        )

        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS parameter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_name TEXT NOT NULL,
                field_value TEXT NOT NULL,
                listing_id INTEGER,
                FOREIGN KEY (listing_id) REFERENCES listing(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            """
        )

        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data BLOB NOT NULL,
                listing_id INTEGER,
                FOREIGN KEY (listing_id) REFERENCES listing(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            """
        )

        logger.info("Tables created.")

        await self.conn.execute(
            """
            CREATE INDEX idx_listing_category_id ON listing(category_id);
            """
        )
        await self.conn.execute(
            """
            CREATE INDEX idx_listing_user_id ON listing(user_id);
            """
        )
        await self.conn.execute(
            """
            CREATE INDEX idx_parameter_listing_id ON parameter(listing_id);
            """
        )
        await self.conn.execute(
            """
            CREATE INDEX idx_media_listing_id ON media(listing_id);
            """
        )

        logger.info("Indexes established.")

        await self.seed_categories()

        logger.info("Categories seeded.")

        await self.conn.commit()

        logger.info("Tables committed.")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
