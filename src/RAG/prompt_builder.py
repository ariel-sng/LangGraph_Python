from src.models.rag_search_result import RAGSearchResult

class PromptBuilder:

    def build(
        self,
        question: str,
        context_chunks: list[RAGSearchResult],
    ) -> str:

        context = "\n\n".join([chunk.document for chunk in context_chunks])
        return f"""
            Respondé utilizando únicamente el contexto provisto.

            <CONTEXT>
            {context}
            </CONTEXT>
            
            <QUESTION>
            {question}
            </QUESTION>
        """