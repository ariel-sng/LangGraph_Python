from abc import ABC, abstractmethod

from chromadb.api.types import (
    Embedding,
    Embeddings,
    Metadata,
)

from src.models.rag_search_result import RAGSearchResult

class VectorStore(ABC):
    '''
        Clase abstracta para manejar el almacenamiento de vectores.
        Quieren SOLID? Acá hay SOLID.
    '''

    @abstractmethod
    def save(
        self,
        embeddings: Embeddings,
        chunks: list[str],
        metadata: Metadata,
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        embedding: Embedding,
        k: int,
    ) -> list[RAGSearchResult]:
        pass