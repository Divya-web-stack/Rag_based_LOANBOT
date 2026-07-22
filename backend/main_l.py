from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import chat, upload, audio, health

app = FastAPI(title="LoanBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route modules
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router,   tags=["Chat"])
app.include_router(upload.router, tags=["Documents"])
app.include_router(audio.router,  tags=["Audio"])