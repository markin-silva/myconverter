import boto3
import os

from botocore.client import Config
from urllib.parse import urlparse, urlunparse

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")
S3_PUBLIC_ENDPOINT = os.getenv("S3_PUBLIC_ENDPOINT", "http://localhost:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minio")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minio123")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "converted-files")

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_PUBLIC_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1"
)

def upload_file_to_s3(file_path: str, key: str):
    s3_client.upload_file(file_path, S3_BUCKET_NAME, key)
    return f"{S3_PUBLIC_ENDPOINT}/{S3_BUCKET_NAME}/{key}"

def generate_presigned_url(key: str, expires_in: int = 3600):
    # Gera URL assinada com endpoint interno (minio:9000)
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in
    )

    # Substitui o host interno (minio:9000) por localhost:9000 visível externamente
    parsed_internal = urlparse(url)
    parsed_public = urlparse(S3_PUBLIC_ENDPOINT)

    corrected_url = urlunparse(parsed_internal._replace(
        netloc=parsed_public.netloc,
        scheme=parsed_public.scheme
    ))

    return corrected_url
