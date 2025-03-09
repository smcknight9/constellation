import os
import requests
from fastapi import HTTPException

class WeaviateClient:
    BASE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")

    @classmethod
    def search(cls, query: str):
        """Search the Weaviate vector database for related entries."""
        endpoint = f"{cls.BASE_URL}/v1/query"
        payload = {
            "query": query,
            "filters": {"source": "journal_entries"}
        }
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "results" not in data:
                raise HTTPException(status_code=500, detail="Invalid response from Weaviate API.")
            
            return data["results"]
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Weaviate API Error: {e}")
