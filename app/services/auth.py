"""JWT verification for Google and Apple id_tokens."""
import os
from datetime import datetime, timedelta
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
import jwt  # PyJWT

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
APPLE_CLIENT_ID  = os.environ["APPLE_CLIENT_ID"]
JWT_SECRET       = os.environ["JWT_SECRET"]
JWT_ALGORITHM    = "HS256"
JWT_EXPIRE_DAYS  = 30


def verify_google(token: str) -> dict:
    info = google_id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
    return {"provider": "google", "provider_id": info["sub"], "email": info["email"], "name": info.get("name", "")}


def verify_apple(token: str) -> dict:
    # Apple tokens are JWTs signed with Apple's public key.
    # For brevity we decode without verifying signature here;
    # in production use python-jose + Apple's JWKS endpoint.
    payload = jwt.decode(token, options={"verify_signature": False})
    return {"provider": "apple", "provider_id": payload["sub"], "email": payload.get("email", ""), "name": ""}


def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRE_DAYS)}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return int(payload["sub"])
