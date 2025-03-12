from fastapi import APIRouter, HTTPException, UploadFile, File
import os

import config
from services.static import static_service

router = APIRouter(
    tags=["static"],
)

@router.post("/upload", response_model=dict)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload a static image file.
    """
    relative_path = await static_service.save_uploaded_file(file)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "path": f"/static/{relative_path}",
        "size": os.path.getsize(config.STATIC_DIR / relative_path)
    }

@router.delete("/delete/{file_path:path}")
async def delete_image(file_path: str):
    """
    Delete an uploaded static image file.
    """
    result = static_service.delete_static_file(file_path)
    if result:
        return {"status": "success", "message": "File deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="File not found.") 