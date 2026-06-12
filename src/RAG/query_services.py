import json
from pathlib import Path

import tiktoken

from src.config.settings import Settings
from src.models.search_result import SearchResult
from src.models.rag_search_result import RAGSearchResult
from src.repositories.vector_store import VectorStore
from src.RAG.embedding_generator import EmbeddingGenerator
from src.RAG.prompt_builder import PromptBuilder
from src.RAG.llm_generator import LLMGenerator 

class RagQueryService:

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
        prompt_builder: PromptBuilder,
        llm_generator: LLMGenerator,
    ):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.prompt_builder = prompt_builder
        self.llm_generator = llm_generator

    def search(
        self,
        question: str,
        k: int = 5,
    ) -> list[RAGSearchResult]:
       
        embedding = self.embedding_generator.generate(  [question] )[0]

        return self.vector_store.search(
            embedding=embedding,
            k=k,
        )
    
    def answer(
        self,
        question: str,
        k: int = 5,
    ) -> SearchResult:
        results = self.search(
            question=question,
            k=k,
        )

        prompt = self._build_prompt_with_limit(
            question=question,
            context_chunks=results,
        )
        
        system_answer = self.llm_generator.generate(
            prompt
        )

        return SearchResult(
            question=question,
            answer=system_answer,
            chunks=results,
        )

    def _build_prompt_with_limit(
        self,
        question: str,
        context_chunks: list[RAGSearchResult],
    ) -> str:
        
        encoder = self._get_token_encoder()
        max_tokens = Settings.MAX_PROMPT_TOKENS
        
        chunks = context_chunks.copy()
        prompt = self.prompt_builder.build(question=question, context_chunks=chunks)
        token_count = self._count_tokens(prompt, encoder)
        
        '''
        Lógica del acotador de prompt: 

        Prompt (pregunta + contexto completo adquirido por RAG)
        ↓
        ¿Excede "max_tokens"?
            ├─ NO → Devuelve el prompt [✓]
            └─ SÍ → Elimina chunks de contexto
                ↓
                ¿Excede "max_tokens"?
                    ├─ NO → Devuelve prompt sin algunos chunks [✓]
                    └─ SÍ → Elimina TODO el contexto
                        ↓
                        ¿Excede "max_tokens"?
                            ├─ NO → Devuelve pregunta sin contexto [✓]
                            └─ SÍ → Acorta la pregunta misma
                                ↓
                                ¿Hay espacio?
                                    ├─ SÍ → Devuelve pregunta acortada [✓]
                                    └─ NO → Error (límite muy pequeño) [X]
        '''
        while token_count > max_tokens and chunks:
            chunks.pop()
            prompt = self.prompt_builder.build(question=question, context_chunks=chunks)
            token_count = self._count_tokens(prompt, encoder)

        if token_count > max_tokens:
            prompt_without_context = self.prompt_builder.build(question=question, context_chunks=[])
            token_count = self._count_tokens(prompt_without_context, encoder)

            if token_count > max_tokens:
                overhead = self._count_tokens(
                    self.prompt_builder.build(question="", context_chunks=[]),
                    encoder,
                )
                remaining_tokens = max_tokens - overhead
                if remaining_tokens <= 0:
                    raise ValueError(
                        "MAX_PROMPT_TOKENS is too small to build a valid prompt."
                    )

                question = self._truncate_text_to_token_limit(
                    question,
                    remaining_tokens,
                    encoder,
                )

            prompt = self.prompt_builder.build(question=question, context_chunks=[])

        return prompt

    def _get_token_encoder(self):
        try:
            return tiktoken.encoding_for_model(self.llm_generator.model)
        except Exception:
            return tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self, text: str, encoder) -> int:
        return len(encoder.encode(text))

    def _truncate_text_to_token_limit(
        self,
        text: str,
        max_tokens: int,
        encoder,
    ) -> str:
        tokens = encoder.encode(text)
        return encoder.decode(tokens[:max_tokens])
    
    def save_rag_result(
        self,
        result: SearchResult,
        output_file: str = Settings.RAG_RESULT_FILE,
    ):
        print("Guardando resultado del RAG en formato JSON...")

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        new_result = {
            "question": result.question,
            "system_answer": result.answer,
            "chunks": [
                {
                    "document": chunk.document,
                    "distance": chunk.distance,
                    "metadata": chunk.metadata,
                }
                for chunk in result.chunks
            ],
        }

        results = []
        if Path(output_file).exists():
            try:
                with open(output_file, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list):
                        results = existing_data
                    else:
                        results = [existing_data]
            except (json.JSONDecodeError, IOError):
                results = []

        results.append(new_result)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print("Archivo guardado con éxito.")
