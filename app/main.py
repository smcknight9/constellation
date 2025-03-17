"""
Main application module.

This module initializes the FastAPI application, sets up startup events,
and includes the API endpoints.
"""

from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.services.weaviate_client import initialize_weaviate_schema

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.

    Initializes the Weaviate schema on startup by importing the schema into
    the Weaviate instance.
    """
    # Initialize Weaviate schema on startup
    print("Running startup event to import Weaviate schema...")
    initialize_weaviate_schema()

# Include the routes defined in endpoints.py
app.include_router(api_router)
