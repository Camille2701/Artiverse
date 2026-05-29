import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile, HTTPException, status

from app.core.config import settings

# Configuration
UPLOAD_DIR = Path("uploads/images")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

# Cached boto3 client (created lazily so the import works without boto3/S3 config).
_s3_client = None


def _get_s3_client():
    """Create (once) and return a boto3 S3 client from settings."""
    global _s3_client
    if _s3_client is None:
        import boto3  # imported lazily so local-only deployments don't need it

        _s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
    return _s3_client


def _s3_public_url(key: str) -> str:
    """Build the public URL for an object stored under ``key``."""
    if settings.S3_PUBLIC_URL:
        return f"{settings.S3_PUBLIC_URL.rstrip('/')}/{key}"
    if settings.S3_ENDPOINT_URL:
        return f"{settings.S3_ENDPOINT_URL.rstrip('/')}/{settings.S3_BUCKET_NAME}/{key}"
    return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"


class StorageService:
    """Image storage service supporting a local filesystem or an S3 backend."""

    @staticmethod
    def init_storage():
        """Create the local upload directory when using the local backend."""
        if settings.STORAGE_BACKEND != "s3":
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _validate(file: UploadFile, contents: bytes) -> str:
        """Validate extension and size; return the lowercased extension."""
        file_ext = Path(file.filename or "").suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_ext} not allowed. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
            )
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Max size: {MAX_FILE_SIZE // (1024 * 1024)}MB"
            )
        return file_ext

    @staticmethod
    async def upload_image(file: UploadFile, folder: str = "media") -> str:
        """
        Upload an image and return the reference to store in the database.

        - Local backend: returns the relative path ("folder/uuid.ext"), served at /uploads.
        - S3 backend: returns the public URL of the uploaded object.
        """
        try:
            contents = await file.read()
            file_ext = StorageService._validate(file, contents)

            unique_filename = f"{uuid.uuid4()}{file_ext}"
            key = f"{folder}/{unique_filename}"
            content_type = file.content_type or _CONTENT_TYPES.get(file_ext, "application/octet-stream")

            if settings.STORAGE_BACKEND == "s3":
                return StorageService._upload_to_s3(contents, key, content_type)
            return StorageService._upload_to_local(contents, key)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Upload failed: {str(e)}"
            )

    @staticmethod
    def _upload_to_local(contents: bytes, key: str) -> str:
        """Persist ``contents`` to the local upload directory and return the key."""
        file_path = UPLOAD_DIR / key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)
        return key

    @staticmethod
    def _upload_to_s3(contents: bytes, key: str, content_type: str) -> str:
        """Upload ``contents`` to S3 under ``key`` and return its public URL."""
        if not settings.S3_BUCKET_NAME:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="S3 backend selected but S3_BUCKET_NAME is not configured"
            )
        _get_s3_client().put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=key,
            Body=contents,
            ContentType=content_type,
        )
        return _s3_public_url(key)

    @staticmethod
    def get_file_path(filename: str) -> Path:
        """Get the full local file path for a stored filename."""
        return UPLOAD_DIR / filename

    @staticmethod
    def _key_from_reference(reference: str) -> str:
        """Derive the S3 object key from a stored reference (URL or key)."""
        if settings.S3_PUBLIC_URL and reference.startswith(settings.S3_PUBLIC_URL):
            return reference[len(settings.S3_PUBLIC_URL):].lstrip("/")
        if reference.startswith("http://") or reference.startswith("https://"):
            # Strip scheme/host and (for path-style URLs) a leading bucket segment.
            path = reference.split("://", 1)[1].split("/", 1)[1] if "/" in reference.split("://", 1)[1] else ""
            if settings.S3_BUCKET_NAME and path.startswith(f"{settings.S3_BUCKET_NAME}/"):
                path = path[len(settings.S3_BUCKET_NAME) + 1:]
            return path
        return reference

    @staticmethod
    def delete_image(filename: str) -> bool:
        """Delete a stored image. Returns True on success, False otherwise."""
        try:
            if settings.STORAGE_BACKEND == "s3":
                if not settings.S3_BUCKET_NAME:
                    return False
                key = StorageService._key_from_reference(filename)
                _get_s3_client().delete_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
                return True

            file_path = StorageService.get_file_path(filename)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False


# Initialize local storage on import (no-op for the S3 backend)
StorageService.init_storage()
