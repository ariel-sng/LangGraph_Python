from pathlib import Path
from typing import Optional, List, Dict, Any

from src.config.settings import Settings


from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def _get_chroma(collection_name: str = "default", persist_dir: Optional[str] = None):
    base_persist = Path(persist_dir) if persist_dir is not None else Path("storage") / "chroma"

    embeddings = OpenAIEmbeddings(model=Settings.EMBEDDING_MODEL)
    chroma = Chroma(persist_directory=str(base_persist), embedding_function=embeddings, collection_name=collection_name)
    return chroma


def retrieve_chunks(
        *,
        query: str, 
        k: int = 5, 
        collection_name: str = "default", 
        persist_dir: Optional[str] = None,
        source: Optional[str] = None,
        ) -> List[Dict[str, Any]]:
    """Return top-k matching chunks from Chroma with their metadata and scores."""
    
    chroma = _get_chroma(collection_name=collection_name, persist_dir=persist_dir)
    #results = chroma.similarity_search_with_score(query, k=k)

    chroma_arg: dict[str, Any] = {"k": k}

    if source:
        chroma_arg["filter"] = {"source": f"{source.lower()}"}

    results = chroma.similarity_search_with_score(
        query,
        **chroma_arg,
    )

    out = []

    for doc, score in results:
        out.append(
            {
                "text": doc.page_content, 
                "metadata": doc.metadata, 
                "score": float(score)
                }
        )
    return out


def answer_query(query: str, k: int = 5, collection_name: str = "default", persist_dir: Optional[str] = None, llm_model: str = "gpt-4o-mini") -> Dict[str, Any]:
    """Retrieve relevant chunks and ask an LLM for an answer composed from those chunks."""
    chroma = _get_chroma(collection_name=collection_name, persist_dir=persist_dir)
    docs = chroma.similarity_search(query, k=k)

    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatOpenAI(model=llm_model, temperature=0)
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=
        """You are an assistant. Use the provided context to answer the question.
        Context:\n{context}\n\nQuestion: {question}\nAnswer:""",
    )

    chain = prompt | llm   
    answer = chain.invoke({"context": context, "question": query})

    return {"question": query, "answer": answer, "context": context, "chunks": [d.metadata for d in docs]}
