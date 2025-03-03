from fastapi import APIRouter

media_router = APIRouter()


@media_router.get("/")
async def greet():
    return {"message": "hello from the media router!"}
