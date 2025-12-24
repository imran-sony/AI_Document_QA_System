from langchain_groq import ChatGroq
from app.core.config import settings

llm = ChatGroq(
    api_key=settings.groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2
)
