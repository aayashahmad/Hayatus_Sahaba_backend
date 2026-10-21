import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
import jwt

load_dotenv()

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 30


def verify_google(token: str) -> dict:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    info = google_id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
    return {"provider": "google", "provider_id": info["sub"], "email": info["email"], "name": info.get("name", "")}


def verify_apple(token: str) -> dict:
    payload = jwt.decode(token, options={"verify_signature": False})
    return {"provider": "apple", "provider_id": payload["sub"], "email": payload.get("email", ""), "name": ""}


def create_access_token(user_id: int) -> str:
    secret = os.environ["JWT_SECRET"]
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRE_DAYS)}
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> int:
    secret = os.environ["JWT_SECRET"]
    payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
    return int(payload["sub"])
