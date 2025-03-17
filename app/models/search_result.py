"""
Search result schema module.

This module defines the schema for search results using Pydantic.
"""

from typing import List, Any
from pydantic import BaseModel

class SearchResult(BaseModel):
    """
    Schema representing the result of a search operation.

    Attributes:
        query (str): The search query string.
        results (List[Any]): A list of search result entries.
            Replace 'Any' with a more specific type if available.
    """
    query: str
    results: List[Any]
