import chromadb


def main() -> None:
    client = chromadb.PersistentClient(
        path="storage/chroma"
    )

    collection = client.get_collection(
        name="documents"
    )

    results = collection.get()

    print(f"Documentos encontrados: {len(results['ids'])}")
    print()

    metadatas = results.get("metadatas")
    documents = results.get("documents")

    for i in range(len(results["ids"])):
        print("=" * 80)

        print(f"ID: {results['ids'][i]}")

        if metadatas is not None and i < len(metadatas):
            print(
                f"Metadata: {metadatas[i]}"
            )

        if documents is not None and i < len(documents):
            print(
                f"Documento:\n{documents[i]}"
            )

        print()

if __name__ == "__main__":
    main()