"""
Weaviate client module.

This module provides a client for interacting with a Weaviate instance.
It includes methods to perform semantic searches for journal entries and
to initialize the Weaviate schema.
"""

import os
import time
import requests
from fastapi import HTTPException

class WeaviateClient:
    """
    Client for interacting with Weaviate.

    Attributes:
        BASE_URL (str): Base URL for the Weaviate instance. Defaults to the
            environment variable "WEAVIATE_URL" or "http://localhost:8080" if not set.
    """
    BASE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")

    @classmethod
    def search_journal_entry(cls, query: str):
        """
        Perform a semantic search for journal entries using Weaviate's GraphQL API.

        Constructs a nearText payload using the provided query and sends a POST
        request to the Weaviate instance. Returns the JSON response containing
        the search results.

        Args:
            query (str): The search query string.

        Returns:
            dict: The JSON response from Weaviate.

        Raises:
            HTTPException: If the request to Weaviate fails.
        """
        # Build a nearText payload using the query
        payload = {
            "query": f"""
            {{
              Get {{
                JournalEntry(nearText: {{ concepts: ["{query}"] }}, limit: 1) {{
                  id
                  _additional {{
                    certainty
                  }}
                }}
              }}
            }}
            """
        }
        endpoint = f"{cls.BASE_URL}/v1/graphql"
        try:
            response = requests.post(endpoint, json=payload)
            print("Raw Weaviate response:", response.text)  # Optional debugging log
            response.raise_for_status()
            return response.json()
        except requests.RequestException as req_excep:
            raise HTTPException(status_code=502, detail=f"Weaviate API Error: {req_excep}")
        
def initialize_weaviate_schema(max_retries: int = 10, delay: int = 3):
    """
    Initialize the Weaviate schema for JournalEntry.

    Attempts to import the JournalEntry schema into Weaviate by sending a POST
    request with the schema definition. Retries the operation if it fails, up to
    the specified number of attempts.

    Args:
        max_retries (int, optional): Maximum number of retry attempts. Defaults to 10.
        delay (int, optional): Delay in seconds between retries. Defaults to 3.

    Returns:
        None

    Side Effects:
        Prints status messages to the console.
    """
    schema_endpoint = f"{WeaviateClient.BASE_URL}/v1/schema"
    # Define the JournalEntry class
    schema_payload = {
        "class": "JournalEntry",
        "description": "A journal entry for second-brain",
        "vectorizer": "text2vec-transformers",
        "properties": [{"name": "content",
                        "dataType": ["text"]}]
        }

    headers = {"Content-Type": "application/json"}
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(schema_endpoint, json=schema_payload, headers=headers)
            response.raise_for_status()
            print("Successfully imported schema into Weaviate")
            return
        except requests.RequestException as req_excep:
            print(f"Attempt {attempt} failed: {req_excep}")
            time.sleep(delay)
    print("Failed to import schema into Weaviate after several attempts.")
