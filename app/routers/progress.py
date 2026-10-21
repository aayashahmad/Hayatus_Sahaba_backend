from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Progress, User
from app.schemas import ProgressIn, ProgressOut
from app.services.deps import current_user

router = APIRouter()

@router.get("/", response_model=list[ProgressOut])
def get_progress(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(Progress).filter_by(user_id=user.id).all()

@router.put("/{vol}", response_model=ProgressOut)
def update_progress(vol: int, body: ProgressIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    prog = db.query(Progress).filter_by(user_id=user.id, vol=vol).first()
    if prog:
        prog.page = body.page
    else:
        prog = Progress(user_id=user.id, vol=vol, page=body.page)
        db.add(prog)
    db.commit()
    db.refresh(prog)
    return prog
