"""
Page routes - template rendering for web pages
"""

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from lazy_crawler.api import config
from lazy_crawler.api.auth import get_current_user_optional
from lazy_crawler.api.database import User
from typing import Optional
import os

router = APIRouter(tags=["pages"])

# Template Engine
templates = Jinja2Templates(directory=config.TEMPLATES_DIR)


@router.get("/")
def read_root(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Home page"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "active_page": "home", "user": current_user}
    )


@router.get("/login")
def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/dashboard")
def read_dashboard(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    """User dashboard"""
    if not current_user:
        return RedirectResponse(url="/login")

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "active_page": "dashboard", "user": current_user},
    )


@router.get("/about")
def read_about(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    """About page"""
    return templates.TemplateResponse(
        "about.html", {"request": request, "active_page": "about", "user": current_user}
    )


@router.get("/contact")
def read_contact(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Contact page"""
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "active_page": "contact", "user": current_user},
    )


@router.get("/privacy")
def read_privacy(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Privacy policy page"""
    return templates.TemplateResponse(
        "privacy.html",
        {"request": request, "active_page": "privacy", "user": current_user},
    )


@router.get("/sitemap.xml")
def get_sitemap():
    """Sitemap for SEO"""
    return FileResponse(os.path.join(config.STATIC_DIR, "sitemap.xml"))


@router.get("/robots.txt")
def get_robots():
    """Robots.txt for search engines"""
    return FileResponse(os.path.join(config.STATIC_DIR, "robots.txt"))
