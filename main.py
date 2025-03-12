from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

import config
from routers import proxy, static, status

# Create FastAPI app
app = FastAPI(
    title="Image Server",
    description="Server for image proxying and static image serving",
    version="1.0.0"
)

# Mount cache and static directories
app.mount("/cache", StaticFiles(directory=config.CACHE_DIR), name="cache")
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")

# Include routers
app.include_router(proxy.router)
app.include_router(static.router)
app.include_router(status.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True)
