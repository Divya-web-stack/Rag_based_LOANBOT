from fastapi import APIRouter
from backend.models.chat import ChatRequest, ChatResponse
from backend.langgraph_agent.graph import run_langgraph_agent
from backend.langgraph_agent.memory import memory_store

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    memory_store.add_user(req.session_id, req.message)  # correct method name
    reply = run_langgraph_agent(req.message, session_id=req.session_id)
    return ChatResponse(reply=reply, session_id=req.session_id)


@router.delete("/chat/{session_id}")
async def clear_history(session_id: str):
    """Clear conversation history for a given session."""
    memory_store.clear(session_id)
    return {"status": "cleared", "session_id": session_id}