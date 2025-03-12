import aiohttp
from fastapi import HTTPException
from pathlib import Path

import config
from services.cache import cache_service

class ProxyService:
    """
    Handles image proxying operations
    """
    
    # Streaming download and cache storage async generator
    async def stream_and_cache_image(self, url: str, cache_path: Path):
        timeout = aiohttp.ClientTimeout(total=config.PROXY_TIMEOUT)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=response.status, detail=f"Failed to fetch original image: {response.reason}")
    
                    # Return streaming response while simultaneously saving to file
                    with open(cache_path, "wb") as f:
                        async for chunk in response.content.iter_any():
                            f.write(chunk)
                            yield chunk
    
                    # Run cache cleanup
                    cache_service.cleanup_cache()
            except aiohttp.ClientError as e:
                raise HTTPException(status_code=500, detail=f"Image request failed: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


proxy_service = ProxyService()
