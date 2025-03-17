"""
Second Brain client module.

This module provides a client for interacting with the Second Brain API.
It includes methods to fetch individual journal entries as well as all entries.
"""

import os
import requests
from fastapi import HTTPException

class SecondBrainClient:
    """
    Client for interacting with the Second Brain API.

    Attributes:
        BASE_URL (str): Base URL for the Second Brain API, read from the environment
            variable "SECOND_BRAIN_API" or defaulting to "http://localhost:8001".
    """
    BASE_URL = os.getenv("SECOND_BRAIN_API", "http://localhost:8001")

    @classmethod
    def get_entry(cls, entry_id: str):
        """
        Fetch a single journal entry from Second Brain by ID.

        Args:
            entry_id (int): The ID of the journal entry.

        Returns:
            dict: The JSON response containing the journal entry data.

        Raises:
            HTTPException: If the request fails.
        """
        endpoint = f"{cls.BASE_URL}/entries/{entry_id}/"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as req_excep:
            raise HTTPException(status_code=502, detail=f"SecondBrain API Error: {req_excep}")

    @classmethod
    def get_entries(cls):
        """
        Fetch all journal entries from Second Brain.

        Returns:
            dict: The JSON response containing all journal entries.

        Raises:
            HTTPException: If the request fails.
        """
        endpoint = f"{cls.BASE_URL}/entries/"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as req_excep:
            raise HTTPException(status_code=502, detail=f"SecondBrain API Error: {req_excep}")
