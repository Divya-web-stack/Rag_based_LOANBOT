from pydantic import BaseModel


class STTResponse(BaseModel):
    text: str


class TTSResponse(BaseModel):
    audio_path: str