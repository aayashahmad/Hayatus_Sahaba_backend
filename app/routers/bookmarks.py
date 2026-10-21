from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bookmark, User
from app.schemas import BookmarkIn, BookmarkOut
from app.services.deps import current_user

router = APIRouter()

@router.get("/", response_model=list[BookmarkOut])
def list_bookmarks(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(Bookmark).filter_by(user_id=user.id).all()

@router.post("/", response_model=BookmarkOut, status_code=201)
def add_bookmark(body: BookmarkIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    bm = Bookmark(user_id=user.id, vol=body.vol, page=body.page)
    db.add(bm)
    db.commit()
    db.refresh(bm)
    return bm

@router.delete("/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    bm = db.get(Bookmark, bookmark_id)
    if not bm or bm.user_id != user.id:
        raise HTTPException(404, "Not found")
    db.delete(bm)
    db.commit()
