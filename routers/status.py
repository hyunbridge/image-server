from fastapi import APIRouter

import config

router = APIRouter(
    tags=["status"],
)

@router.get("/status")
async def get_status():
    """
    Return server status information.
    """
    cache_size = sum(f.stat().st_size for f in config.CACHE_DIR.rglob("*") if f.is_file())
    static_size = sum(f.stat().st_size for f in config.STATIC_DIR.rglob("*") if f.is_file())
    
    return {
        "status": "running",
        "cache_size": cache_size,
        "cache_limit": config.STORAGE_LIMIT,
        "static_size": static_size,
        "cache_files": len(list(config.CACHE_DIR.rglob("*")))
    } 