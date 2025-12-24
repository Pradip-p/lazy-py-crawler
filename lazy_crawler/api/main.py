"""
FastAPI Application Entry Point
Minimal configuration - all routes and settings are modularized
"""

from lazy_crawler.api.database import init_db
from lazy_crawler.api import config
from lazy_crawler.api.routers import auth, ai, ds, contact, pages, data, health
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on application startup"""
    await init_db()
    yield


# Initialize FastAPI app
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)

app.add_middleware(GZipMiddleware, minimum_size=config.GZIP_MIN_SIZE)


# Include all Routers
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(ds.router)
app.include_router(contact.router)
app.include_router(pages.router)
app.include_router(data.router)
app.include_router(health.router)


# Mount Static Files
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
