from fastapi import APIRouter

field_router = APIRouter()


@field_router.get("/")
async def greet():
    return {"message": "hello from the fields router!"}
