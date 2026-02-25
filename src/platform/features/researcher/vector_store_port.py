from abc import ABC, abstractmethod
from src.platform.core.entities import SearchResult
from typing import List, Dict

class VectorStorePort(ABC):
    @abstractmethod
    async def upsert_documents(self, documents: List[Dict[str, str]]):
        """Ingestion Function for Marketing Data"""
        pass
    
    @abstractmethod
    async def hybrid_search(self, query: str, limit: int = 5) -> List[SearchResult]:
        """Perform semantic and keyword search"""
        pass