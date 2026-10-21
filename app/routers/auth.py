from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import TokenIn, TokenOut, UserOut
from app.services.auth import verify_google, verify_apple, create_access_token
from app.services.deps import current_user

router = APIRouter()

@router.post("/login", response_model=TokenOut)
def login(body: TokenIn, db: Session = Depends(get_db)):
    if body.provider == "google":
        info = verify_google(body.id_token)
    elif body.provider == "apple":
        info = verify_apple(body.id_token)
    else:
        raise HTTPException(400, "Unknown provider")

    user = db.query(User).filter_by(provider_id=info["provider_id"]).first()
    if not user:
        user = User(**info)
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"access_token": create_access_token(user.id)}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user
