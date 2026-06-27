from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.category_router import (
    router as category_router
)
app = FastAPI(
    title="Assessment Portal API",
    version="1.0.0"
)
# Allowed frontend origins
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(
    category_router
)

@app.get("/")
async def home():
    """
    Root endpoint to check if the API is running
    """
    return {
        "message": "Assessment Portal API Running"
    }