from pydantic import BaseModel
from typing import List, Optional

class Entry(BaseModel):
    id: int
    title: str
    content: str
    created_at: str  # Or use `datetime` if needed

class SearchResult(BaseModel):
    query: str
    results: List[Entry]
