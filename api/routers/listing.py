from fastapi import APIRouter

listing_router = APIRouter()


@listing_router.get("/")
async def greet():
    return {"message": "hello from the listings router!"}
