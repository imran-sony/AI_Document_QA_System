from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    source: str | None = None

class QueryResponse(BaseModel):
    answer: str
