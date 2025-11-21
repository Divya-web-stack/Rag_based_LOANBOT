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
    try:
        data = await request.json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return {"reply": "Please enter a valid message."}

        print(f"🟦 User: {user_message}")

        response = run_master_agent(user_message)

        # If LLM returns dict / None / unexpected type → force string
        if not isinstance(response, str):
            try:
                response = str(response)
            except:
                response = "⚠️ Unable to generate response."

        print(f"🟩 Bot: {response}")

        return {"reply": response}

    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return {"reply": "Server Error: " + str(e)}

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
