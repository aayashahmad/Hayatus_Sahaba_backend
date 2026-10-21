import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()


def _client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY"],
        aws_secret_access_key=os.environ["R2_SECRET_KEY"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


def public_audio_url(vol: int, page: int) -> str:
    return f"{os.environ['R2_PUBLIC_URL']}/audio/vol{vol}/{page:04d}.mp3"


def public_timing_url(vol: int, page: int) -> str:
    return f"{os.environ['R2_PUBLIC_URL']}/audio/vol{vol}/{page:04d}.json"
