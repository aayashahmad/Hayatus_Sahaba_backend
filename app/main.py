from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routers import auth, text, audio, bookmarks, progress

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hayatus Sahaba API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/api/auth",      tags=["auth"])
app.include_router(text.router,      prefix="/api/text",      tags=["text"])
app.include_router(audio.router,     prefix="/api/audio",     tags=["audio"])
app.include_router(bookmarks.router, prefix="/api/bookmarks", tags=["bookmarks"])
app.include_router(progress.router,  prefix="/api/progress",  tags=["progress"])

@app.get("/health")
def health():
    return {"status": "ok"}
