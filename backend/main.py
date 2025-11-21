from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.master_agent import run_master_agent
from backend.rag_chromadb import query_docs
from backend.audio_utils import speech_to_text, text_to_speech
import shutil
import os

app = FastAPI()

# ✅ Enable CORS so frontend (HTML/JS) can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure required directories exist
os.makedirs("backend/data/policies", exist_ok=True)
os.makedirs("backend/data", exist_ok=True)

@app.get("/")
def home():
    """Health check endpoint"""
    return {"status": "LoanBot backend running successfully 🚀"}

# ✅ Chat endpoint (Frontend → Backend)
# ✅ Chat endpoint (Frontend → Backend)
@app.post("/chat")
async def chat(request: Request):
    """Handles chat messages from frontend"""
    try:
        data = await request.json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return {"reply": "Please enter a valid message."}

        print(f"🟦 User: {user_message}")
        reply = run_master_agent(user_message)
        print(f"🟩 Final Bot Reply: {reply}")

        # ✅ Always return clean JSON — no print output included
        return {"reply": str(reply).strip()}

    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return {"reply": f"Server Error: {str(e)}"}

# ✅ Upload policy PDF/text data for RAG
@app.post("/upload_policy")
async def upload_policy(file: UploadFile = File(...)):
    """Uploads a new policy document and reindexes it in ChromaDB"""
    try:
        path = f"backend/data/policies/{file.filename}"
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Optional: Automatically rebuild RAG index
        from backend.rag_index_builder import create_rag_index
        create_rag_index()

        return {"message": f"{file.filename} uploaded and indexed successfully ✅"}
    except Exception as e:
        return {"message": f"Error while uploading: {e}"}

# ✅ Speech-to-text (STT)
@app.post("/stt")
async def stt(file: UploadFile = File(...)):
    """Convert speech (WAV file) to text"""
    try:
        path = "backend/data/temp.wav"
        with open(path, "wb") as f:
            f.write(await file.read())

        text = speech_to_text(path)
        return {"text": text}
    except Exception as e:
        return {"error": f"STT conversion failed: {e}"}

# ✅ Text-to-speech (TTS)
@app.post("/tts")
async def tts(text: str = Form(...)):
    """Convert text reply into audio"""
    try:
        path = text_to_speech(text)
        return {"audio_path": path}
    except Exception as e:
        return {"error": f"TTS generation failed: {e}"}
