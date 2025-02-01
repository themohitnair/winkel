from fastapi import Depends, APIRouter
from database.initialize import Database

router = APIRouter(prefix="/metric", tags=["Metrics"])


@router.get("/")
async def greet(db: Database = Depends(Database)):
    return {"message": "Hi from metric router."}
