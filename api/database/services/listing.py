from database.init import Database
from typing import List

from models.listing import Listing


class ListingService(Database):
    def __init__(self, db_path: str = "database.db"):
        super().__init__(db_path)

    async def create_listing(
        self,
        listing_name: str,
        listing_price: float,
        category_id: int,
        user_id: int,
        desc: str,
    ):
        await self.connect()
        try:
            async with self.conn.execute(
                """
                INSERT INTO listing (listing_name, listing_price, category_id, "desc", user_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (listing_name, listing_price, category_id, desc, user_id),
            ) as cursor:
                last_row_id = cursor.lastrowid
            await self.conn.commit()
            return last_row_id
        except Exception as e:
            raise RuntimeError(f"Failed to create listing: {e}")

    async def get_listing_by_id(self, listing_id: int) -> Listing:
        await self.connect()

        try:
            async with self.conn.execute(
                "SELECT * FROM listing WHERE id = ?", (listing_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                raise ValueError(f"Listing with ID {listing_id} not found.")

            return Listing(
                id=row[0],
                listing_name=row[1],
                listing_price=row[2],
                category_id=row[3],
                desc=row[4],
                user_id=row[5],
            )
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve listing with ID {listing_id}: {e}")

    async def get_all_listing(self) -> List[Listing]:
        await self.connect()

        try:
            async with self.conn.execute("SELECT * FROM listing") as cursor:
                rows = await cursor.fetchall()

            if not rows:
                return []

            return [
                Listing(
                    id=row[0],
                    listing_name=row[1],
                    listing_price=row[2],
                    category_id=row[3],
                    desc=row[4],
                    user_id=row[5],
                )
                for row in rows
            ]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve all listings: {e}")

    async def update_listing(
        self,
        listing_id: int,
        listing_name: str,
        listing_price: float,
        category_id: int,
        desc: str,
        user_id: int,
    ):
        await self.connect()

        try:
            result = await self.conn.execute(
                """
                UPDATE listing
                SET listing_name = ?, listing_price = ?, category_id = ?, "desc" = ?, user_id = ?
                WHERE id = ?
                """,
                (listing_name, listing_price, category_id, desc, user_id, listing_id),
            )
            await self.conn.commit()

            if result.rowcount == 0:
                raise ValueError(f"Listing with ID {listing_id} not found for update.")
        except Exception as e:
            raise RuntimeError(f"Failed to update listing with ID {listing_id}: {e}")

    async def delete_listing(self, listing_id: int):
        await self.connect()

        try:
            result = await self.conn.execute(
                "DELETE FROM listing WHERE id = ?", (listing_id,)
            )
            await self.conn.commit()

            if result.rowcount == 0:
                raise ValueError(
                    f"Listing with ID {listing_id} not found for deletion."
                )
        except Exception as e:
            raise RuntimeError(f"Failed to delete listing with ID {listing_id}: {e}")
