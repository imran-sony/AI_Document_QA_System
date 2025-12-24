from fastapi import FastAPI
from app.api.routes import router
from app.rag.vectorstore import load_vectorstore
from app.rag.retriever import get_retriever

app = FastAPI(title="AI Document Q&A System")
app.include_router(router)

@app.on_event("startup")
async def startup():

    vectorstore = load_vectorstore()


    retriever = get_retriever(vectorstore, k=5)

    app.state.vectorstore = vectorstore
    app.state.retriever = retriever

