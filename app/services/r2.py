"""Cloudflare R2 — generate presigned audio URLs."""
import os
import boto3
from botocore.client import Config

R2_ACCOUNT_ID   = os.environ["R2_ACCOUNT_ID"]
R2_ACCESS_KEY   = os.environ["R2_ACCESS_KEY"]
R2_SECRET_KEY   = os.environ["R2_SECRET_KEY"]
R2_BUCKET       = os.environ["R2_BUCKET"]
R2_PUBLIC_URL   = os.environ["R2_PUBLIC_URL"]   # e.g. https://pub.example.com

_client = boto3.client(
    "s3",
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="auto",
)


def public_audio_url(vol: int, page: int) -> str:
    key = f"audio/vol{vol}/{page:04d}.mp3"
    return f"{R2_PUBLIC_URL}/{key}"


def public_timing_url(vol: int, page: int) -> str:
    key = f"audio/vol{vol}/{page:04d}.json"
    return f"{R2_PUBLIC_URL}/{key}"
