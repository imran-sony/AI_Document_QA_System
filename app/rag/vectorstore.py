import os
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from app.rag.embeddings import embeddings

VECTOR_PATH = "data/vectorstore"

def load_vectorstore():
    if os.path.exists(VECTOR_PATH):
        return FAISS.load_local(
            VECTOR_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    dim = len(embeddings.embed_query("dimension check"))
    index = faiss.IndexFlatL2(dim)

    return FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )

def save_vectorstore(vectorstore):
    vectorstore.save_local(VECTOR_PATH)
