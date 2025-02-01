from fastapi import Depends, APIRouter
from database.initialize import Database

router = APIRouter(prefix="/parameter", tags=["Parameters"])


@router.get("/")
async def greet(db: Database = Depends(Database)):
    return {"message": "Hi from parameter router."}
