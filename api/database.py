import libsql_client as libsql

import logging.config
from config import LOG_CONFIG


logger = logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, url: str, auth_token: str | None = None):
        self.client: libsql.Client = libsql.create_client(
            url,
            auth_token=auth_token,
        )

    logger.info("Creating tables...")

    async def create_tables(self):
        categories = [
            "Books",
            "Stationery",
            "Electronics",
            "Furniture",
            "Clothing",
            "Accessories",
            "Sporting Goods",
            "Kitchenware",
            "Miscellaneous",
        ]

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

        category_tuples = [(category,) for category in categories]

        placeholders = ",".join(["(?)"] * len(categories))

        flat_category_params = [cat for tup in category_tuples for cat in tup]

        await self.client.execute(
            f"INSERT OR IGNORE INTO category (name) VALUES {placeholders}",
            args=flat_category_params,
        )

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS user (
            auth_id TEXT PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE CHECK (LENGTH(phone) = 10),
            rating_buy REAL DEFAULT 0.0 CHECK (rating_buy >= 0 AND rating_buy <= 5),
            rating_sell REAL DEFAULT 0.0 CHECK (rating_sell >= 0 AND rating_sell <= 5),
            status TEXT CHECK (status IN ('active', 'banned', 'deleted')) DEFAULT 'active',
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'utc'))
        )
        """)

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS listing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            title TEXT,
            description TEXT,
            category_id INTEGER,
            price REAL CHECK (price >= 0),
            condition TEXT CHECK (condition IN ('new', 'usable', 'poor')) NOT NULL,
            status TEXT CHECK (status IN ('available', 'sold')) DEFAULT 'available',
            created_at TEXT DEFAULT (datetime('now', 'utc')),
            updated_at TEXT DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (user_id) REFERENCES user(auth_id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL
        )
        """)

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS media (
            listing_id INTEGER,
            key TEXT,
            value TEXT,
            FOREIGN KEY (listing_id) REFERENCES listing(id) ON DELETE CASCADE
        )
        """)

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS field (
            listing_id INTEGER,
            key TEXT,
            value TEXT,
            PRIMARY KEY (listing_id, key),
            FOREIGN KEY (listing_id) REFERENCES listing(id) ON DELETE CASCADE
        );
        """)

        await self.client.execute("""
        CREATE TRIGGER IF NOT EXISTS update_user_timestamp
        AFTER UPDATE ON user
        FOR EACH ROW
        WHEN NEW.updated_at = OLD.updated_at  -- Prevent infinite loop
        BEGIN
            UPDATE user SET updated_at = datetime('now', 'utc')
            WHERE auth0_id = NEW.auth0_id;
        END
        """)

        await self.client.execute("""
        CREATE TRIGGER IF NOT EXISTS update_listing_timestamp
        AFTER UPDATE ON listing
        FOR EACH ROW
        WHEN NEW.updated_at = OLD.updated_at
        BEGIN
            UPDATE listing SET updated_at = datetime('now', 'utc')
            WHERE id = NEW.id;
        END
        """)
