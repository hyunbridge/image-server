from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from services.cache import cache_service
from services.proxy import proxy_service

router = APIRouter(
    prefix="/p",
    tags=["proxy"],
)

@router.get("/{full_path:path}")
async def serve_cached_image(full_path: str, request: Request):
    """
    Proxy and cache remote images.
    """
    query_params = str(request.url.query)
    original_url = f"https://{full_path}" + (f"?{query_params}" if query_params else "")
    cached_file_path = cache_service.get_cache_path(f"https://{full_path}")

    # Return cached file if it exists
    if cache_service.is_cache_valid(cached_file_path):
        return StreamingResponse(open(cached_file_path, "rb"), media_type="image/*")
    
    # Download from remote if cache doesn't exist or is expired
    return StreamingResponse(
        proxy_service.stream_and_cache_image(original_url, cached_file_path), 
        media_type="image/*"
    ) 