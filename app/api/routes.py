from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pathlib import Path
import uuid
import aiofiles
import traceback

from app.api.schemas import QueryRequest, QueryResponse
from app.core.task_queue import enqueue_task
from app.rag.ingest import ingest_document
from app.rag.vectorstore import save_vectorstore
from app.rag.retriever import get_retriever
from app.agent.graph import build_graph
from app.agent.llm import llm

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Upload endpoint
@router.post("/upload")
async def upload_document(request: Request, file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith((".pdf", ".docx")):
            raise HTTPException(status_code=400, detail="Only PDF or DOCX allowed")

        file_id = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / file_id

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                await f.write(chunk)

        async def process():
            vectorstore = request.app.state.vectorstore
            await ingest_document(str(file_path), vectorstore, original_filename=file.filename)
            save_vectorstore(vectorstore)

        await enqueue_task(process())

        return {
            "status": "success",
            "filename": file.filename,
            "message": "Document uploaded and indexed successfully"
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# Query endpoint
@router.post("/query", response_model=QueryResponse)
async def query_document(request: Request, request_data: QueryRequest):
    try:
        retriever = request.app.state.retriever

 
        agent = build_graph(llm, retriever, source=request_data.source, top_k=5)

        state = {"question": request_data.question, "context": "", "answer": ""}
        result = agent.invoke(state)
        return {"answer": result["answer"]}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
