from routers.field import field_router
from routers.listing import listing_router
from routers.media import media_router
from routers.user import user_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(field_router, prefix="/fields", tags=["Fields"])
app.include_router(listing_router, prefix="/listings", tags=["Listings"])
app.include_router(media_router, prefix="/media", tags=["Media"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
async def greet():
    return {"message": "winkel says hello!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
