from fastapi import Depends, APIRouter
from database.initialize import Database

router = APIRouter(prefix="/member", tags=["Members"])


@router.get("/")
async def greet(db: Database = Depends(Database)):
    return {"message": "Hi from member router."}
