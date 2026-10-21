from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.r2 import public_audio_url, public_timing_url

router = APIRouter()

@router.get("/{vol}/{page}/mp3")
def get_audio(vol: int, page: int):
    return RedirectResponse(public_audio_url(vol, page), status_code=302)

@router.get("/{vol}/{page}/timing")
def get_timing(vol: int, page: int):
    return RedirectResponse(public_timing_url(vol, page), status_code=302)
