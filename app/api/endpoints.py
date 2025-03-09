from fastapi import APIRouter, HTTPException, Query
from app.models.search_result import SearchResult
from app.services.weaviate_client import WeaviateClient
from app.services.second_brain import SecondBrainClient

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """ Health Check Endpoint """
    return {"status": "ok"}

@router.get("/search", response_model=SearchResult, tags=["Search"])
async def search(query: str = Query(..., description="Search query string")):
    """
    Search for entries using semantic search.

    - **query**: The search query string.
    """
    try:
        # Perform semantic search using Weaviate
        semantic_results = WeaviateClient.search(query)
        
        # Enrich the results with detailed data from Second Brain
        enriched_entries = [
            SecondBrainClient.get_entry(result.get("id"))
            for result in semantic_results if result.get("id")
        ]
        return SearchResult(query=query, results=[entry for entry in enriched_entries if entry])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
