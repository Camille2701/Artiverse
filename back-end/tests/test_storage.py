import io

import pytest
from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.services import storage_service
from app.services.storage_service import StorageService


def _upload_file(filename: str, content: bytes = b"fake-image-bytes") -> UploadFile:
    return UploadFile(filename=filename, file=io.BytesIO(content))


class FakeS3Client:
    """Minimal stand-in for a boto3 S3 client that records calls."""

    def __init__(self):
        self.put_calls = []
        self.delete_calls = []

    def put_object(self, **kwargs):
        self.put_calls.append(kwargs)

    def delete_object(self, **kwargs):
        self.delete_calls.append(kwargs)


class TestLocalStorage:
    async def test_upload_returns_key_and_writes_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "local")
        monkeypatch.setattr(storage_service, "UPLOAD_DIR", tmp_path)

        key = await StorageService.upload_image(_upload_file("poster.png"), folder="covers")

        assert key.startswith("covers/")
        assert key.endswith(".png")
        assert (tmp_path / key).exists()

    async def test_invalid_extension_rejected(self, monkeypatch):
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "local")
        with pytest.raises(HTTPException) as exc:
            await StorageService.upload_image(_upload_file("malware.exe"))
        assert exc.value.status_code == 400

    async def test_oversized_file_rejected(self, monkeypatch):
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "local")
        big = b"x" * (storage_service.MAX_FILE_SIZE + 1)
        with pytest.raises(HTTPException) as exc:
            await StorageService.upload_image(_upload_file("huge.jpg", big))
        assert exc.value.status_code == 400

    async def test_delete_local_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "local")
        monkeypatch.setattr(storage_service, "UPLOAD_DIR", tmp_path)
        target = tmp_path / "media" / "x.png"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"data")

        assert StorageService.delete_image("media/x.png") is True
        assert not target.exists()
        assert StorageService.delete_image("media/missing.png") is False


class TestS3Storage:
    async def test_upload_to_s3_returns_public_url(self, monkeypatch):
        fake = FakeS3Client()
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "s3")
        monkeypatch.setattr(settings, "S3_BUCKET_NAME", "artiverse-media")
        monkeypatch.setattr(settings, "AWS_REGION", "eu-west-3")
        monkeypatch.setattr(settings, "S3_ENDPOINT_URL", None)
        monkeypatch.setattr(settings, "S3_PUBLIC_URL", None)
        monkeypatch.setattr(storage_service, "_get_s3_client", lambda: fake)

        url = await StorageService.upload_image(_upload_file("poster.png"), folder="covers")

        assert len(fake.put_calls) == 1
        put = fake.put_calls[0]
        assert put["Bucket"] == "artiverse-media"
        assert put["ContentType"] == "image/png"
        assert put["Key"].startswith("covers/")
        assert url == f"https://artiverse-media.s3.eu-west-3.amazonaws.com/{put['Key']}"

    async def test_upload_to_s3_uses_public_base_url(self, monkeypatch):
        fake = FakeS3Client()
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "s3")
        monkeypatch.setattr(settings, "S3_BUCKET_NAME", "artiverse-media")
        monkeypatch.setattr(settings, "S3_PUBLIC_URL", "https://cdn.artiverse.app/")
        monkeypatch.setattr(storage_service, "_get_s3_client", lambda: fake)

        url = await StorageService.upload_image(_upload_file("a.webp"))

        assert url.startswith("https://cdn.artiverse.app/media/")

    async def test_upload_to_s3_without_bucket_fails(self, monkeypatch):
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "s3")
        monkeypatch.setattr(settings, "S3_BUCKET_NAME", None)
        monkeypatch.setattr(storage_service, "_get_s3_client", lambda: FakeS3Client())

        with pytest.raises(HTTPException) as exc:
            await StorageService.upload_image(_upload_file("a.png"))
        assert exc.value.status_code == 500

    async def test_delete_from_s3(self, monkeypatch):
        fake = FakeS3Client()
        monkeypatch.setattr(settings, "STORAGE_BACKEND", "s3")
        monkeypatch.setattr(settings, "S3_BUCKET_NAME", "artiverse-media")
        monkeypatch.setattr(settings, "S3_PUBLIC_URL", "https://cdn.artiverse.app/")
        monkeypatch.setattr(storage_service, "_get_s3_client", lambda: fake)

        assert StorageService.delete_image("https://cdn.artiverse.app/covers/abc.png") is True
        assert fake.delete_calls[0]["Key"] == "covers/abc.png"
