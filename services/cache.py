import hashlib
import time
from pathlib import Path
from urllib.parse import urlparse

import config

class CacheService:
    """
    Handles caching operations for proxied images
    """
    
    def __init__(self):
        # Create directory
        config.CACHE_DIR.mkdir(exist_ok=True)
    
    # Cache key generation (excluding query parameters, using SHA-256 hash)
    def get_cache_path(self, url: str) -> Path:
        parsed_url = urlparse(url)
        clean_url = parsed_url.netloc + parsed_url.path  # Keep domain + path (exclude query parameters)
        hash_key = hashlib.sha256(clean_url.encode()).hexdigest()
        subdir = config.CACHE_DIR / hash_key[:2]  # Create subdirectory with first 2 characters
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / hash_key
    
    # Cache cleanup function
    def cleanup_cache(self):
        files = list(config.CACHE_DIR.rglob("*"))
        if not files:
            return
    
        # Calculate total cache size
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        if total_size <= config.STORAGE_LIMIT:
            return
    
        # Sort and delete old files
        files.sort(key=lambda f: f.stat().st_atime)  # Sort by last access time
        while total_size > config.STORAGE_LIMIT and files:
            oldest = files.pop(0)
            try:
                total_size -= oldest.stat().st_size
                oldest.unlink()
            except Exception as e:
                print(f"Failed to delete cache file {oldest}: {e}")
    
    # Cache validity check
    def is_cache_valid(self, cache_path: Path) -> bool:
        if not cache_path.exists():
            return False
            
        if config.CACHE_TTL is None:
            return True
            
        return (time.time() - cache_path.stat().st_mtime) < config.CACHE_TTL

cache_service = CacheService()
