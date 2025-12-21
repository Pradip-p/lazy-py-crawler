from lazy_crawler.api.db import init_db, engine
from sqlalchemy import text
from lazy_crawler.api.auth import get_current_user_optional
from lazy_crawler.api.routers import auth, ai, ds
from lazy_crawler.api.models import User
from fastapi import FastAPI, HTTPException, Query, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lazy Crawler API",
    description="API to access data scraped by Lazy Crawler",
    version="1.0.0",
)

# Configure CORS to allow credentials
# Read allowed origins from environment variable (comma-separated list)
# Example: CORS_ORIGINS=https://pradipthapa.info.np,https://www.pradipthapa.info.np
cors_origins_str = os.getenv("CORS_ORIGINS", "*")
cors_origins = (
    [origin.strip() for origin in cors_origins_str.split(",")]
    if cors_origins_str != "*"
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize DB on Startup
@app.on_event("startup")
async def on_startup():
    await init_db()


# Include Routers
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(ds.router)

# Template Engine
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "lazy_crawler")

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

# Mount Static Files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def read_root(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    return templates.TemplateResponse(
        "index.html", {"request": request, "active_page": "home", "user": current_user}
    )


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard")
def read_dashboard(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/login")

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "active_page": "dashboard", "user": current_user},
    )


@app.get("/about")
def read_about(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    return templates.TemplateResponse(
        "about.html", {"request": request, "active_page": "about", "user": current_user}
    )


@app.get("/contact")
def read_contact(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "active_page": "contact", "user": current_user},
    )


@app.get("/privacy")
def read_privacy(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    return templates.TemplateResponse(
        "privacy.html",
        {"request": request, "active_page": "privacy", "user": current_user},
    )


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Docker and Nginx monitoring.
    """
    status = {"status": "healthy", "checks": {}}
    try:
        # Check MongoDB connection
        client.admin.command("ping")
        status["checks"]["mongodb"] = "connected"
    except Exception as e:
        status["status"] = "unhealthy"
        status["checks"]["mongodb"] = f"disconnected: {str(e)}"

    try:
        # Check Postgres connection
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        status["checks"]["postgres"] = "connected"
    except Exception as e:
        status["status"] = "unhealthy"
        status["checks"]["postgres"] = f"disconnected: {str(e)}"

    return status


@app.get("/collections")
def list_collections():
    """
    List all available scraped datasets (collections).
    """
    collections = db.list_collection_names()
    return {"collections": collections}


@app.get("/data/{collection_name}")
def get_data(
    collection_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: Optional[str] = None,
):
    """
    Retrieve items from a specific collection with pagination and basic search.
    """
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")

    collection = db[collection_name]

    # Basic search filter if 'q' is provided (search in all string fields)
    filter_query = {}
    if q:
        filter_query = {"$or": [{"$text": {"$search": q}}]}
        # Note: Text index must be created in MongoDB for this to work perfectly.
        # Fallback for simple regex if index is not present:
        # filter_query = {"$or": [{"title": {"$regex": q, "$options": "i"}}, {"description": {"$regex": q, "$options": "i"}}]}

    skip = (page - 1) * page_size
    items = list(collection.find(filter_query).skip(skip).limit(page_size))

    # Convert MongoDB _id to string
    for item in items:
        if "_id" in item:
            item["_id"] = str(item["_id"])

    total_count = collection.count_documents(filter_query)

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_items": total_count,
        "total_pages": (total_count + page_size - 1) // page_size,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
