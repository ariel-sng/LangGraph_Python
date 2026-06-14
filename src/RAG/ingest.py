from pathlib import Path
from typing import List, Dict, Optional

from src.config.settings import Settings

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader

def _load_markdown_sections(file_path: Path) -> List[Dict[str, str]]:
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    sections: List[Dict[str, str]] = []
    current_title = "root"
    buffer: List[str] = []

    for line in lines:
        if line.lstrip().startswith("#"):
            # flush buffer
            if buffer:
                sections.append({"section": current_title, "text": "\n".join(buffer).strip()})
                buffer = []
            # new title is the heading text without leading #
            current_title = line.lstrip().lstrip("#").strip() or "section"
        else:
            buffer.append(line)

    if buffer:
        sections.append({"section": current_title, "text": "\n".join(buffer).strip()})

    return sections


def _chunk_text(text: str, method: str = "fixed", chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    if method == "sentence":
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        return splitter.split_text(text)

    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)


def ingest_md(
    file_path: str,
    collection_name: str = "default",
    persist_dir: Optional[str] = None,
    chunk_method: str = "fixed",
    chunk_size: int = 500,
    chunk_overlap: int = 100,
):
    """Ingest a markdown file into ChromaDB using LangChain wrappers.

    - `file_path`: path to .md file
    - `collection_name`: chroma collection name
    - `persist_dir`: where Chroma persists (defaults to storage/chroma)
    - `chunk_method`: 'fixed' or 'sentence'
    - `chunk_size` / `chunk_overlap`: splitter params
    """

    md_path = Path(file_path)
    if not md_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    base_persist = Path(persist_dir) if persist_dir is not None else Path("storage") / "chroma"
    base_persist.mkdir(parents=True, exist_ok=True)

    embeddings = OpenAIEmbeddings(model=Settings.EMBEDDING_MODEL)

    loader = TextLoader(str(md_path), encoding="utf-8")
    docs = loader.load()


    chunks = _chunk_text(
        docs[0].page_content,
        method=chunk_method,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    texts = chunks
    
    metadatas = [{"source": md_path.name} for _ in chunks]
    # persist to Chroma via langchain wrapper
    chroma = Chroma.from_texts(
        texts,
        embeddings,
        metadatas=metadatas,
        persist_directory=str(base_persist),
        collection_name=collection_name,
    )

    return chroma
