from fastapi import FastAPI

from app.routers.auth_router import router as auth_router


app = FastAPI(
    title="Assessment Portal API"
)

app.include_router(auth_router)


@app.get("/")
async def home():
    return {
        "message": "Assessment Portal API Running"
    }