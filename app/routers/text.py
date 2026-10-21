import json, pathlib
from fastapi import APIRouter, HTTPException

router = APIRouter()

TEXT_DIR = pathlib.Path("public/text")

@router.get("/{vol}/{page}")
def get_text(vol: int, page: int):
    path = TEXT_DIR / f"vol{vol}" / f"{page:04d}.json"
    if not path.exists():
        raise HTTPException(404, "Page not found")
    return json.loads(path.read_text())
