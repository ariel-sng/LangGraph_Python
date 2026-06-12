from abc import ABC, abstractmethod

from chromadb.api.types import Embeddings
from openai import OpenAI

from typing import cast

from chromadb.api.types import Embeddings

class EmbeddingGenerator(ABC):

    @abstractmethod
    def generate(self, texts: list[str]) -> Embeddings:
        pass


class OpenAIEmbeddingGenerator(EmbeddingGenerator):

    def __init__(
        self,
        client: OpenAI,
        model: str = "text-embedding-3-small",
    ):
        self.client = client
        self.model = model

    def generate(
        self,
        texts: list[str],
    ) -> Embeddings:
        
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return cast(Embeddings, [item.embedding for item in response.data],)