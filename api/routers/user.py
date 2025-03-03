from fastapi import APIRouter

user_router = APIRouter()


@user_router.get("/")
async def greet():
    return {"message": "hello from the user router!"}
