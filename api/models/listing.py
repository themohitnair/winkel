from pydantic import BaseModel

class Listing(BaseModel):
    id: int
    listing_name: str
    listing_price: float
    category_id: int
    desc: str
    user_id: int
