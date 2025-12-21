import os
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lazy Crawler API",
    description="API to access data scraped by Lazy Crawler",
    version="1.0.0",
)

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
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "active_page": "home"}
    )


@app.get("/dashboard")
def read_dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "active_page": "dashboard"}
    )


@app.get("/about")
def read_about(request: Request):
    return templates.TemplateResponse(
        "about.html", {"request": request, "active_page": "about"}
    )


@app.get("/contact")
def read_contact(request: Request):
    return templates.TemplateResponse(
        "contact.html", {"request": request, "active_page": "contact"}
    )


@app.get("/privacy")
def read_privacy(request: Request):
    return templates.TemplateResponse(
        "privacy.html", {"request": request, "active_page": "privacy"}
    )


@app.get("/health")
def health_check():
    """
    Health check endpoint for Docker and Nginx monitoring.
    """
    try:
        # Check MongoDB connection
        client.admin.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "service": "lazy-crawler-api",
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


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
