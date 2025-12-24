from app.rag.loader import load_document
from app.rag.chunker import chunk_documents
from pathlib import Path

async def ingest_document(file_path: str, vectorstore, original_filename: str | None = None):
    docs = load_document(file_path)
    chunks = chunk_documents(docs)

    if not chunks:
        print(f"No chunks found in {file_path}")
        return

    filename = original_filename or Path(file_path).name

    for chunk in chunks:
        chunk.metadata["source"] = filename
       
        print("Chunk content:", chunk.page_content[:100], "...", "source:", chunk.metadata["source"])

    vectorstore.add_documents(chunks)
