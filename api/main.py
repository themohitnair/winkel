from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def greet():
    return {"message": "Hello from winkel!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(port=8000, host="localhost", app="main:app", reload=True)
