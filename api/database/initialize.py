import asyncpg
import os
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()


class Database:
    def __init__(self):
        self.pool = None
        self.logger = logging.getLogger(__name__)

        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")

        if not all([self.db_user, self.db_name]):
            raise ValueError("Missing required database environment variables.")

    async def create_db(self, connection: asyncpg.Connection):
        try:
            self.logger.info(f"Creating db {self.db_name}...")
            await connection.execute(f"CREATE DATABASE {self.db_name};")
        except asyncpg.exceptions.DuplicateDatabaseError:
            self.logger.warning(f"Database {self.db_name} already exists.")
        except asyncpg.exceptions.PostgresError as e:
            self.logger.error(f"Error creating database {self.db_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error while creating database {self.db_name}: {e}"
            )
            raise

    async def seed_categories(self, connection: asyncpg.Connection):
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

            await connection.executemany(
                """
            INSERT INTO category (name)
            VALUES ($1)
            ON CONFLICT (name) DO NOTHING;
            """,
                categories,
            )

            self.logger.info("Categories seeded successfully.")

        except asyncpg.exceptions.UniqueViolationError as e:
            self.logger.warning(f"Unique violation error while seeding categories: {e}")
        except Exception as e:
            self.logger.error(f"Error seeding categories: {e}", exc_info=True)
            raise

    async def create_tables(self, connection: asyncpg.Connection):
        try:
            async with connection.transaction():
                await connection.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id SERIAL PRIMARY KEY,
                    num_members INTEGER DEFAULT 0,
                    num_listings INTEGER DEFAULT 0,
                    num_sold_listings INTEGER DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                await connection.execute("""
                CREATE TABLE IF NOT EXISTS member (
                    firebase_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL UNIQUE,
                    last_name TEXT NOT NULL UNIQUE,
                    phone_number TEXT NOT NULL UNIQUE,
                    university_serial_number TEXT NOT NULL,
                    verified BOOLEAN DEFAULT FALSE,
                    seller_rating DECIMAL(3,2) DEFAULT 5.0 CHECK (seller_rating BETWEEN 1 AND 5),
                    num_seller_ratings INTEGER DEFAULT 0,
                    buyer_rating DECIMAL(3,2) DEFAULT 5.0 CHECK (buyer_rating BETWEEN 1 AND 5),
                    num_buyer_ratings INTEGER DEFAULT 0,
                    sold_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                await connection.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT NOT NULL UNIQUE
                );
                """)
                await connection.execute("""
                CREATE TABLE IF NOT EXISTS listing (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    title TEXT NOT NULL,
                    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
                    description TEXT NOT NULL,
                    member_id TEXT NOT NULL,
                    category_id UUID NOT NULL,
                    condition TEXT CHECK (condition IN ('new', 'like_new', 'good', 'fair', 'poor')),
                    status TEXT CHECK (status IN ('available', 'sold')) DEFAULT 'available',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (member_id) REFERENCES member(firebase_id) ON DELETE CASCADE ON UPDATE CASCADE
                );
                """)
                await connection.execute("""
                CREATE TABLE IF NOT EXISTS media (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    listing_id UUID NOT NULL,
                    image_url TEXT NOT NULL,
                    FOREIGN KEY (listing_id) REFERENCES listing(id) ON DELETE CASCADE ON UPDATE CASCADE
                );
                """)
                await connection.execute("""
                CREATE TABLE IF NOT EXISTS param (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    listing_id UUID NOT NULL,
                    field_name TEXT NOT NULL,
                    field_value TEXT NOT NULL,
                    FOREIGN KEY (listing_id) REFERENCES listing(id) ON DELETE CASCADE ON UPDATE CASCADE
                );
                """)
                self.logger.info("Tables created!")
                await connection.execute("""
                    CREATE INDEX IF NOT EXISTS idx_member_phone_number ON member(phone_number);
                    CREATE INDEX IF NOT EXISTS idx_member_uni_serial_number ON member(university_serial_number);
                    CREATE INDEX IF NOT EXISTS idx_member_seller_rating ON member(seller_rating);
                    CREATE INDEX IF NOT EXISTS idx_member_buyer_rating ON member(buyer_rating);
                    CREATE INDEX IF NOT EXISTS idx_category_name ON category(name);
                    CREATE INDEX IF NOT EXISTS idx_listing_member_id ON listing(member_id);
                    CREATE INDEX IF NOT EXISTS idx_listing_category_id ON listing(category_id);
                    CREATE INDEX IF NOT EXISTS idx_listing_status ON listing(status);
                    CREATE INDEX IF NOT EXISTS idx_listing_price ON listing(price);
                    CREATE INDEX IF NOT EXISTS idx_listing_created_at ON listing(created_at);
                    CREATE INDEX IF NOT EXISTS idx_media_listing_id ON media(listing_id);
                    CREATE INDEX IF NOT EXISTS idx_param_listing_id ON param(listing_id);
                    CREATE INDEX IF NOT EXISTS idx_param_field_name ON param(field_name);
                """)
                self.logger.info("Indices created!")
        except asyncpg.exceptions.DuplicateTableError as e:
            self.logger.warning(f"Table already exists: {e}")
        except Exception as e:
            self.logger.error(f"Error creating tables: {e}", exc_info=True)
            raise

    async def db_exists(self, connection: asyncpg.Connection) -> bool:
        try:
            databases = await connection.fetch("SELECT datname FROM pg_database;")
            existing_databases = [db["datname"] for db in databases]
            if self.db_name not in existing_databases:
                self.logger.info(f"Database {self.db_name} does not exist.")
                return False
            else:
                self.logger.info(f"Database {self.db_name} already exists.")
                return True
        except asyncpg.exceptions.PostgresError as e:
            self.logger.error(f"Error checking if database {self.db_name} exists: {e}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error while checking if database {self.db_name} exists: {e}"
            )
            raise

    async def connect(self, retries: int = 5, delay: int = 2):
        attempt = 1
        while attempt <= retries:
            try:
                connection = await asyncpg.connect(
                    user=self.db_user,
                    host="127.0.0.1",
                    port=5432,
                    database="postgres",
                )

                if not await self.db_exists(connection):
                    await self.create_db(connection)

                await connection.close()

                self.pool = await asyncpg.create_pool(
                    user=self.db_user,
                    host="127.0.0.1",
                    port=5432,
                    database=self.db_name,
                    min_size=15,
                    max_size=50,
                    command_timeout=30,
                )
                self.logger.info("Database connection pool established!")
                break
            except Exception as e:
                self.logger.error(f"Error connecting to the database: {e}")
                if attempt < retries:
                    self.logger.info(
                        f"Retrying in {delay} seconds... (Attempt {attempt}/{retries})"
                    )
                    await asyncio.sleep(delay * attempt)
                attempt += 1

        if self.pool is None:
            self.logger.error(
                "Max retries reached. Unable to establish database connection."
            )
            raise Exception("Unable to connect to the database.")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.logger.info("Database connection pool flushed!")
