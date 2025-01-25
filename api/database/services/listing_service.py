from sqlmodel import Session, UUID
from typing import Optional, List
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
        try:
            listing = Listing(
                listing_name=listing_name,
                listing_price=listing_price,
                category_id=category_id,
                user_id=user_id,
                desc=desc,
            )
            repo = ListingRepository(self.session)
            return repo.create(listing)
        except Exception as e:
            return e

    def get_listing_by_id(self, listing_id: int) -> Optional[Listing]:
        return self.listing_repository.get(listing_id)

    def get_all_listing(self) -> List[Listing]:
        return self.listing_repository.get_all()

    def update_listing(
        self,
        listing_id: UUID,
        listing_name: str,
        listing_price: float,
        category_id: UUID,
        desc: str,
        user_id: UUID,
    ):
        try:
            listing = self.listing_repository.get(id)
        except Exception as e:
            return e
