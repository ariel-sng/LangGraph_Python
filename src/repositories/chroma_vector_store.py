from typing import cast
from uuid import uuid4

import chromadb
from chromadb.api.types import (
    Embedding, 
    Embeddings,
    Metadata,
    Metadatas,
)

from src.repositories.vector_store import VectorStore
from src.models.rag_search_result import RAGSearchResult

class ChromaVectorStore(VectorStore):

    def __init__(
        self,
        persist_directory: str = "storage/chroma",
        collection_name: str = "documents"
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection_name = collection_name
        self.collection_metadata = {
            "hnsw:space": "cosine"
        }

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine"
            }
        )

    def save(
        self,
        embeddings: Embeddings,
        chunks: list[str],
        metadata: Metadata,
    ) -> None:

        ids = [
            str(uuid4())
            for _ in chunks
        ]

        metadatas: Metadatas = cast(
            Metadatas,
            [
                {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                }
                for i in range(len(chunks))
            ]
        )

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )


    def reset(self) -> None:
        self.client.delete_collection(
            self.collection.name
        )

        self.collection = self.client.get_or_create_collection(
            name     =   self.collection.name,
            metadata =   self.collection_metadata,
        )
    
    def search(
        self,
        embedding: Embedding,
        k: int,
    ) -> list[RAGSearchResult]:
        
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
            include=[
                "documents",
                "distances",
                "metadatas",
            ],
        )

        documents = results.get("documents")
        distances = results.get("distances")
        metadatas = results.get("metadatas")

        if (
            documents is None
            or distances is None
            or metadatas is None
        ):
            return []

        documents_list = documents[0]
        distances_list = distances[0]
        metadatas_list = metadatas[0]

        return [
            RAGSearchResult(
                document=document,
                distance=distance,
                metadata=metadata,
            )
            for document, distance, metadata in zip(
                documents_list,
                distances_list,
                metadatas_list,
            )
        ]