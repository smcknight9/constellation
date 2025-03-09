import os
import requests
from fastapi import HTTPException

class SecondBrainClient:
    BASE_URL = os.getenv("SECOND_BRAIN_API", "http://localhost:8001")

    @classmethod
    def get_entry(cls, entry_id: int):
        """Fetch a single entry from Second Brain by ID."""
        endpoint = f"{cls.BASE_URL}/entries/{entry_id}/"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"SecondBrain API Error: {e}")

    @classmethod
    def get_entries(cls):
        """Fetch all entries from Second Brain."""
        endpoint = f"{cls.BASE_URL}/entries/"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"SecondBrain API Error: {e}")
