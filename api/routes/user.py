from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/")
async def user_greet():
    return {"message": "User router says hi!"}
