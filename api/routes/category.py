from fastapi import Depends, APIRouter
from database.initialize import Database

router = APIRouter(prefix="/category", tags=["Categories"])


@router.get("/")
async def greet(db: Database = Depends(Database)):
    return {"message": "Hi from category router."}
