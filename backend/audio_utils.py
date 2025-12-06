from vosk import Model, KaldiRecognizer
from TTS.api import TTS
import wave, json

stt_model = Model(lang="en-us")
tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC")

def speech_to_text(path):
    wf = wave.open(path, "rb")
    rec = KaldiRecognizer(stt_model, wf.getframerate())
    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0: break
        if rec.AcceptWaveform(data):
            text += json.loads(rec.Result())["text"]
    return text

def text_to_speech(text, out_path="backend/data/output.wav"):
    tts_model.tts_to_file(text=text, file_path=out_path)
    return out_path
