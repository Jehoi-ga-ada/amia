from typing import Dict, List

from src.platform.core.entities import SearchResult
from src.platform.features.researcher.vector_store_port import VectorStorePort
from qdrant_client import QdrantClient, models

class QdrantAdapter(VectorStorePort):
    def __init__(self, host: str = "localhost", port: int = 6333) -> None:
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = "marketing_intelligence"
        
    def initialize_collection(self):
        """
        Sets up the collection with Hybrid Search support
        """
        
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                self.collection_name,
                vectors_config={
                    "dense": models.VectorParams(
                        size=384, 
                        distance=models.Distance.COSINE
                    )
                },
                sparse_vectors_config={
                    "sparse": models.SparseVectorParams(
                        index=models.SparseIndexParams(
                            on_disk=True
                        )
                    )
                }
            )
        
    async def upsert_documents(self, documents: List[Dict[str, str]]):
        pass
    
    async def hybrid_search(self, query: str, limit: int = 5) -> List[SearchResult]:
        """Implements Hybrid Search
        1. Dense Vector (Semantic Meaning)
        2. Sparse Vector/Full-text (Keyword matching)

        Args:
            query (str): _description_
            limit (int, optional): _description_. Defaults to 5.

        Returns:
            List[SearchResult]: _description_
        """
        
        response = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                models.Prefetch(
                    query=query,
                    using="dense",
                    limit=20
                ),
                models.Prefetch(
                    query=query,
                    using="sparse",
                    limit=20
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=limit
        )
        
        results = []
        for point in response.points:
            payload = point.payload or {} 
            
            results.append(
                SearchResult(
                    title=payload.get("title", "No Title"),
                    content=payload.get("text", "No Content"),
                    source_url=payload.get("url", "No URL"),
                    score=point.score
                )
            )
            
        return results