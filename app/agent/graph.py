from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    question: str
    context: str
    answer: str

def build_graph(llm, retriever, source: str | None = None, top_k: int = 5):
    def retrieve(state: AgentState):
        
        docs = retriever.get_relevant_documents(
            state["question"],
            filter={"source": source} if source else None
        )

        docs = docs[:top_k] if docs else []

        if not docs:
            state["context"] = ""
        else:
            state["context"] = "\n---\n".join(d.page_content for d in docs)

        
        print(f"Retrieved {len(docs)} chunks for question '{state['question']}'")
        for d in docs:
            print("Source:", d.metadata.get("source"), "Content:", d.page_content[:100])
        return state

    def generate(state: AgentState):
        if not state["context"]:
            state["answer"] = (
                "No content found for the given document. "
                "Please check the filename or upload the document."
            )
            return state

       
        prompt = f"""
You are an AI assistant of a document question-answering system. 
Answer the question based ONLY on the context below.
Do NOT include any information that is not in the context.
Do NOT guess or use external knowledge.
Be concise and factual.

Context:
{state['context']}

Question:
{state['question']}

Answer:
"""
        state["answer"] = llm.invoke(prompt).content
        return state

    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")

    return graph.compile()
