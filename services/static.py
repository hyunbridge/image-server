from pathlib import Path
from fastapi import HTTPException, UploadFile
import shutil
import os
import mimetypes
from uuid import uuid4

import config

class StaticService:
    """
    Handles static file operations
    """
    
    def __init__(self):
        # Create static directory
        config.STATIC_DIR.mkdir(exist_ok=True)
        
        # File extension validation
        self.ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}
    
    def is_valid_image(self, filename: str) -> bool:
        """
        Check if file has an allowed image extension
        """
        ext = os.path.splitext(filename.lower())[1]
        return ext in self.ALLOWED_EXTENSIONS
    
    # File upload handler
    async def save_uploaded_file(self, file: UploadFile) -> str:
        """
        Save uploaded file and return its relative path
        """
        if not self.is_valid_image(file.filename):
            raise HTTPException(status_code=400, detail="File format not allowed")
        
        # Generate unique filename
        ext = os.path.splitext(file.filename)[1]
        new_filename = f"{uuid4()}{ext}"
        
        # Create year/month based directory structure
        from datetime import datetime
        now = datetime.now()
        year_month = now.strftime("%Y/%m")
        save_dir = config.STATIC_DIR / year_month
        save_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = save_dir / new_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return relative path of the file ("/static/2023/01/filename.jpg" format)
        return f"{year_month}/{new_filename}"
    
    # Delete file
    def delete_static_file(self, file_path: str) -> bool:
        """
        Delete a static file and return success status
        """
        full_path = config.STATIC_DIR / file_path
        
        if not full_path.exists():
            return False
            
        if not full_path.is_relative_to(config.STATIC_DIR):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        try:
            full_path.unlink()
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

static_service = StaticService()
