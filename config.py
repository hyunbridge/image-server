from typing import Optional
from pathlib import Path
import os

# Basic configuration
CACHE_DIR = Path("cache")
STATIC_DIR = Path("static")

# Cache settings
CACHE_TTL: Optional[int] = None  # in seconds (None means unlimited)
STORAGE_LIMIT = 500 * 1024 * 1024  # 500MB limit

# Server settings
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8000))

# Proxy settings
PROXY_TIMEOUT = 60  # in seconds 