import os
import shutil

from fastapi import APIRouter, File, UploadFile
from backend.langgraph_agent.graph import graph
from backend.rag_chromadb import rebuild_index
from backend.models.upload import UploadResponse

router = APIRouter()


def verify_document(file_path: str) -> bool:
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(script_dir, "data", "documents")
    os.makedirs(docs_dir, exist_ok=True)
    file_path = os.path.join(docs_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if not verify_document(file_path):
        return UploadResponse(
            status="error",
            message=f"Uploaded file {file.filename} failed verification.",
        )

    rebuild_index()

    state = {
        "session_id": "default",
        "user_query": f"A new document '{file.filename}' has been uploaded. Summarise it briefly.",
        "uploaded_file": file.filename,
        "upload_verified": True,
        "rag_context": "",
        "messages": [],
        "final_response": "",
    }
    result = graph.invoke(state)

    return UploadResponse(
        status="success",
        message=f"File {file.filename} uploaded, verified, and indexed.",
        reply=result.get("final_response", ""),
    )