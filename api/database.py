import libsql_client as libsql
import asyncio
# from config import TURSO_AUTH, TURSO_URL


class Database:
    def __init__(self, url: str, auth_token: str | None = None):
        self.client: libsql.Client = libsql.create_client(
            url,
            auth_token=auth_token,
        )

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
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

        category_tuples = [(category,) for category in categories]

        placeholders = ",".join(["(?)"] * len(categories))

        flat_category_params = [cat for tup in category_tuples for cat in tup]

        await self.client.execute(
            f"INSERT OR IGNORE INTO categories (name) VALUES {placeholders}",
            args=flat_category_params,
        )

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS user (
            auth0_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            email TEXT UNIQUE,
            usn TEXT UNIQUE,
            rating_buy REAL CHECK (rating_buy >= 0 AND rating_buy <= 5),
            rating_sell REAL CHECK (rating_sell >= 0 AND rating_sell <= 5)
        )
        """)

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS listing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            title TEXT,
            category_id INTEGER,
            price REAL CHECK (price >= 0),
            FOREIGN KEY (user_id) REFERENCES user(auth0_id),
            FOREIGN KEY (category_id) REFERENCES category(id)
        )
        """)

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS media (
            listing_id INTEGER,
            key TEXT,
            value TEXT,
            FOREIGN KEY (listing_id) REFERENCES listing(id)
        )
        """)

        await self.client.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            listing_id INTEGER,
            key TEXT,
            value TEXT,
            PRIMARY KEY (listing_id, key),
            FOREIGN KEY (listing_id) REFERENCES listing(id)
        );
        """)


if __name__ == "__main__":
    db = Database("file:local.db")
    asyncio.run(db.create_tables())
