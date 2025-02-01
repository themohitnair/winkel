from fastapi import Depends, APIRouter
from database.initialize import Database

router = APIRouter(prefix="/media", tags=["Media"])


@router.get("/")
async def greet(db: Database = Depends(Database)):
    return {"message": "Hi from media router."}
