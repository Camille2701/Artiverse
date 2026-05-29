import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from typing import Optional

# Configuration
UPLOAD_DIR = Path("uploads/images")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


class StorageService:
    """Simple local file storage service."""
    
    @staticmethod
    def init_storage():
        """Create upload directory if it doesn't exist."""
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    async def upload_image(file: UploadFile, folder: str = "media") -> str:
        """
        Upload image and return filename.
        
        Args:
            file: UploadFile from FastAPI
            folder: Subdirectory (media, avatars, etc)
        
        Returns:
            Filename (relative path) to store in database
        """
        try:
            # Validate file type by extension
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File type {file_ext} not allowed. Allowed: {ALLOWED_EXTENSIONS}"
                )
            
            # Read file into memory
            contents = await file.read()
            
            # Validate file size
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
                )
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            folder_path = UPLOAD_DIR / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            
            file_path = folder_path / unique_filename
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(contents)
            
            # Return relative path for database
            return f"{folder}/{unique_filename}"
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Upload failed: {str(e)}"
            )
    
    @staticmethod
    def get_file_path(filename: str) -> Path:
        """Get full file path from database filename."""
        return UPLOAD_DIR / filename
    
    @staticmethod
    def delete_image(filename: str) -> bool:
        """Delete image file."""
        try:
            file_path = StorageService.get_file_path(filename)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False


# Initialize storage on import
StorageService.init_storage()
