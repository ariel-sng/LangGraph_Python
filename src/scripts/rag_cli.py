"""CLI for ingesting and retrieving from the RAG pipeline.

Usable via:
    uv run python -m src.scripts.rag_cli ingest <file> [--collection name]
    uv run python -m src.scripts.rag_cli retrieve "question" [--k 5]
"""
import argparse
from pathlib import Path

from src.RAG.ingest import ingest_md
# from src.RAG.retrieve import retrieve_chunks, answer_query


def main():
    parser = argparse.ArgumentParser(prog="rag_cli")
    sub = parser.add_subparsers(dest="cmd")

    parser = argparse.ArgumentParser(prog="rag_cli")

    parser.add_argument(
        "--method",
        choices=["fixed", "sentence"],
        default="fixed",
        help="Chunking method",
    )
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--chunk-overlap", type=int, default=100)

    args = parser.parse_args()
    documents_path = Path("documents")

    if not documents_path.exists() or not documents_path.is_dir():
        raise SystemExit(f"Directory not found: {documents_path}")

    md_files = list(documents_path.glob("*.md"))

    if not md_files:
        raise SystemExit(f"No markdown files found in {documents_path}")

    for file_path in md_files:
        print(f"Ingesting {file_path}")

        ingest_md(
            str(file_path),
            chunk_method=args.method,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )

    print(f"\nSuccessfully ingested {len(md_files)} file(s).")
    '''elif args.cmd == "retrieve":
        if args.answer:
            out = answer_query(args.query, k=args.k, collection_name=args.collection)
            print("Answer:\n", out.get("answer"))
        else:
            chunks = retrieve_chunks(args.query, k=args.k, collection_name=args.collection)
            for i, c in enumerate(chunks, 1):
                sec = c.get("metadata", {}).get("section")
                print(f"[{i}] section={sec} score={c.get('score'):.4f}\n{c.get('text')[:500]}\n---")'''

if __name__ == "__main__":
    main()
