import os

from fastapi import APIRouter, File, Form, UploadFile
from backend.audio_utils import speech_to_text, text_to_speech
from backend.models.audio import STTResponse, TTSResponse

router = APIRouter()


@router.post("/stt", response_model=STTResponse)
async def stt(file: UploadFile = File(...)):
    """Convert speech (WAV file) to text."""
    try:
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        temp_dir = os.path.join(script_dir, "data")
        os.makedirs(temp_dir, exist_ok=True)
        path = os.path.join(temp_dir, "temp.wav")

        with open(path, "wb") as f:
            f.write(await file.read())

        text = speech_to_text(path)
        return STTResponse(text=text)
    except Exception as e:
        return STTResponse(text=f"STT conversion failed: {e}")


@router.post("/tts", response_model=TTSResponse)
async def tts(text: str = Form(...)):
    """Convert text reply into audio."""
    try:
        path = text_to_speech(text)
        return TTSResponse(audio_path=path)
    except Exception as e:
        return TTSResponse(audio_path=f"TTS generation failed: {e}")