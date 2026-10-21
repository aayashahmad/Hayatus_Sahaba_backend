from datetime import datetime
from pydantic import BaseModel

class TokenIn(BaseModel):
    provider: str  # "google" | "apple"
    id_token: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    provider: str
    created_at: datetime
    model_config = {"from_attributes": True}

class BookmarkIn(BaseModel):
    vol: int
    page: int

class BookmarkOut(BookmarkIn):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class ProgressIn(BaseModel):
    vol: int
    page: int

class ProgressOut(ProgressIn):
    updated_at: datetime
    model_config = {"from_attributes": True}
