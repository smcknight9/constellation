from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI()

# Include the routes defined in endpoints.py
app.include_router(api_router)
