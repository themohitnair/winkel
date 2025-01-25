from sqlmodel import Session
from typing import Sequence
from database.repository import ListingRepository
from database.models import Listing


class ListingService:
    def __init__(self, session: Session):
        self.session = session
        self.listing_repository = ListingRepository(self.session)

    def create_listing(
        self,
        listing_name: str,
        listing_price: float,
        category_id: int,
        user_id: int,
        desc: str,
    ) -> Listing:
        listing = Listing(
            listing_name=listing_name,
            listing_price=listing_price,
            category_id=category_id,
            user_id=user_id,
            desc=desc,
        )
        return self.listing_repository.create(listing)

    def get_listing_by_id(self, listing_id: int) -> Listing:
        try:
            listing = self.listing_repository.get(listing_id)
            return listing
        except Exception as e:
            raise e

    def get_all_listing(self) -> Sequence[Listing]:
        return self.listing_repository.get_all()

    def update_listing(
        self,
        listing_id: int,
        listing_name: str,
        listing_price: float,
        category_id: int,
        desc: str,
        user_id: int,
    ) -> Listing:
        try:
            listing = self.listing_repository.get(listing_id)
            listing.listing_name = listing_name
            listing.listing_price = listing_price
            listing.category_id = category_id
            listing.desc = desc
            listing.user_id = user_id
            return self.listing_repository.update(listing)
        except Exception as e:
            raise e

    def delete_listing(self, listing_id: int):
        try:
            listing = self.listing_repository.get(listing_id)
            return self.listing_repository.delete(listing)
        except Exception as e:
            raise e
