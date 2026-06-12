from chromadb.api.types import Metadata

from src.repositories.vector_store import VectorStore
from src.utils.document_loader import DocumentLoader
from src.RAG.embedding_generator import EmbeddingGenerator
from src.utils.text_chunker import TextChunker


class RagIngestionService:

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: TextChunker,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
    ):
        self.loader = loader
        self.chunker = chunker
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def ingest(
        self,
        file_path: str,
        metadata: Metadata | None = None,
    ) -> None:

        text = self.loader.load(file_path)

        chunks = self.chunker.split(text)

        embeddings = self.embedding_generator.generate(
            chunks
        )

        self.vector_store.save(
            embeddings=embeddings,
            chunks=chunks,
            metadata=metadata or {},
        )