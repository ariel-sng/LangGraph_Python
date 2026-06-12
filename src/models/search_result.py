from dataclasses import dataclass

from src.models.rag_search_result import RAGSearchResult

@dataclass
class SearchResult:
    question: str
    answer: str
    chunks: list[RAGSearchResult]