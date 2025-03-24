"""
API endpoints module.

This module defines FastAPI endpoints for health checks and search operations.
It leverages Weaviate for semantic search and the Second Brain API for enriching search results.
"""

from fastapi import APIRouter, HTTPException, Query
from app.models.search_result import SearchResult
from app.services.weaviate_client import WeaviateClient
from app.services.second_brain import SecondBrainClient

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health Check Endpoint.

    Returns:
        dict: A JSON object indicating the status of the application.
    """
    return {"status": "ok"}

@router.get("/search", response_model=SearchResult, tags=["Search"])
async def search(query: str = Query(..., description="Search query string")):
    """
    Search for journal entries using semantic search.

    This endpoint performs a semantic search using Weaviate and enriches the results
    with data from Second Brain.

    Args:
        query (str): The search query string.

    Returns:
        SearchResult: A model containing the original query and a list of enriched results.

    Raises:
        HTTPException: If an error occurs during the search process.
    """
    try:
        semantic_results = WeaviateClient.search_journal_entry(query)
        enriched_entries = [
            SecondBrainClient.get_entry(result.get("id"))
            for result in semantic_results if result.get("id")
        ]
        return SearchResult(query=query, results=[entry for entry in enriched_entries if entry])
    except Exception as exc: 
        raise HTTPException(status_code=500, detail=str(exc))
