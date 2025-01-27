import aiosqlite
from typing import Optional
import logging
from aiosqlite import OperationalError

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = "database.db"):
        self.db_path: str = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        try:
            self.conn = await aiosqlite.connect(self.db_path)

            await self.conn.execute("PRAGMA foreign_keys = ON")
            await self.conn.commit()
            logger.info("Database connection established. ")
        except OperationalError as e:
            logger.info(f"SQLite Database connection error: {e}")
        except Exception as e:
            logger.info(f"Unknown Database Error: {e}")

    async def close(self):
        if self.conn:
            await self.conn.close()
            logger.info("Database connection closed. ")

    async def seed_categories(self):
        try:
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
                "INSERT OR IGNORE INTO category (name) VALUES (?)", categories
            )
            await self.conn.commit()
        except OperationalError as e:
            logger.info(f"SQLite Database connection error: {e}")
        except Exception as e:
            logger.info(f"Unknown Database Error: {e}")

    async def init_db(self):
        try:
            await self.connect()

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
                    rating REAL NOT NULL DEFAULT 0.0
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

            await self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS otp_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    otp_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN DEFAULT FALSE
                )
                """
            )

            logger.info("Tables created.")

            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_listing_category_id ON listing(category_id);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_listing_user_id ON listing(user_id);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_parameter_listing_id ON parameter(listing_id);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_media_listing_id ON media(listing_id);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_user_uni_serial_number ON user(uni_serial_number);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_user_dob ON user(date_of_birth);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_otp_email_expiry ON otp_tokens(email, expires_at, used);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_otp_expires ON otp_tokens(expires_at);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_listing_price ON listing(listing_price);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_listing_name ON listing(listing_name);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_parameter_field ON parameter(field_name);"
            )
            await self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_category_name ON category(name);"
            )

            logger.info("Indices established.")

            await self.seed_categories()

            logger.info("Categories seeded.")

            await self.conn.commit()

            logger.info("transaction committed.")
        except OperationalError as e:
            logger.info(f"SQLite Database connection error: {e}")
        except Exception as e:
            logger.info(f"Unknown Database Error: {e}")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
