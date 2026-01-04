"""
Page routes - template rendering for web pages
"""

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse, Response
from lazy_crawler.app import config
from lazy_crawler.app.auth import get_current_user_optional
from lazy_crawler.app.database import User, get_session, BlogPost
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional
import os
import markdown_it

router = APIRouter(tags=["pages"])

# Template Engine
templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

# Markdown Filter
md = markdown_it.MarkdownIt()


def markdown_filter(text):
    if not text or not isinstance(text, str):
        return ""
    try:
        return md.render(text)
    except Exception:
        return text


templates.env.filters["markdown"] = markdown_filter


@router.get("/")
async def read_root(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_session),
):
    """Home page"""
    # Fetch latest 3 published blog posts
    statement = (
        select(BlogPost)
        .where(BlogPost.published == True)
        .order_by(BlogPost.created_at.desc())
        .limit(3)
    )
    results = await session.exec(statement)
    latest_posts = results.all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "active_page": "home",
            "user": current_user,
            "latest_posts": latest_posts,
        },
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


@router.get("/faq")
def read_faq(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    """FAQ page"""
    return templates.TemplateResponse(
        "faq.html", {"request": request, "active_page": "faq", "user": current_user}
    )


@router.get("/company")
def read_company(
    request: Request, current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Company page (Teams + Careers)"""
    team_members = [
        {
            "name": "Tilak Pathak",
            "role": "Founder & CEO",
            "image": "https://ui-avatars.com/api/?name=Tilak+Pathak&background=4a154b&color=fff",
        },
        {
            "name": "Sarah Chen",
            "role": "CTO",
            "image": "https://ui-avatars.com/api/?name=Sarah+Chen&background=1264a3&color=fff",
        },
        {
            "name": "James Wilson",
            "role": "Head of Product",
            "image": "https://ui-avatars.com/api/?name=James+Wilson&background=2eb67d&color=fff",
        },
        {
            "name": "Emily Rodriguez",
            "role": "VP of Sales",
            "image": "https://ui-avatars.com/api/?name=Emily+R&background=e01e5a&color=fff",
        },
        {
            "name": "Emily Wilson",
            "role": "Data aquistion Lead",
            "image": "https://ui-avatars.com/api/?name=Emily+Wilson&background=2eb67d&color=fff",
        },
        {
            "name": "William Lee",
            "role": "Lead Data Scientist",
            "image": "https://ui-avatars.com/api/?name=William+Lee&background=e01e5a&color=fff",
        },
    ]

    job_openings = [
        {
            "title": "Senior Python Engineer",
            "department": "Engineering",
            "location": "Remote (Global)",
            "tags": ["Full-time", "Senior"],
        },
        {
            "title": "Data Solutions Architect",
            "department": "Solutions",
            "location": "Sydney / Remote",
            "tags": ["Full-time", "Mid-Senior"],
        },
        {
            "title": "Product Designer (UI/UX)",
            "department": "Design",
            "location": "New York / Remote",
            "tags": ["Contract", "Mid-Level"],
        },
    ]

    return templates.TemplateResponse(
        "company.html",
        {
            "request": request,
            "active_page": "company",
            "user": current_user,
            "team_members": team_members,
            "job_openings": job_openings,
        },
    )


@router.get("/sitemap.xml")
async def get_sitemap(session: AsyncSession = Depends(get_session)):
    """Dynamic Sitemap for SEO"""
    base_url = "https://crawlio.org"
    static_pages = [
        {"loc": "/", "changefreq": "daily", "priority": "1.0"},
        {"loc": "/about", "changefreq": "monthly", "priority": "0.8"},
        {"loc": "/contact", "changefreq": "monthly", "priority": "0.7"},
        {"loc": "/privacy", "changefreq": "monthly", "priority": "0.5"},
        {"loc": "/register", "changefreq": "monthly", "priority": "0.8"},
        {"loc": "/company", "changefreq": "monthly", "priority": "0.7"},
        {"loc": "/blog", "changefreq": "daily", "priority": "0.8"},
        {"loc": "/faq", "changefreq": "monthly", "priority": "0.6"},
    ]

    # Fetch all published blog posts
    statement = select(BlogPost).where(BlogPost.published == True)
    results = await session.exec(statement)
    blog_posts = results.all()

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # Add static pages
    for page in static_pages:
        xml_content += f"    <url>\n"
        xml_content += f"        <loc>{base_url}{page['loc']}</loc>\n"
        xml_content += f"        <changefreq>{page['changefreq']}</changefreq>\n"
        xml_content += f"        <priority>{page['priority']}</priority>\n"
        xml_content += f"    </url>\n"

    # Add blog posts
    for post in blog_posts:
        xml_content += f"    <url>\n"
        xml_content += f"        <loc>{base_url}/blog/{post.slug}</loc>\n"
        xml_content += (
            f"        <lastmod>{post.created_at.strftime('%Y-%m-%d')}</lastmod>\n"
        )
        xml_content += f"        <changefreq>weekly</changefreq>\n"
        xml_content += f"        <priority>0.7</priority>\n"
        xml_content += f"    </url>\n"

    xml_content += "</urlset>"

    return Response(content=xml_content, media_type="application/xml")


@router.get("/robots.txt")
def get_robots():
    """Robots.txt for search engines"""
    return FileResponse(os.path.join(config.STATIC_DIR, "robots.txt"))


@router.get("/ads.txt")
def get_ads():
    """Google AdSense ads.txt"""
    return FileResponse(os.path.join(config.STATIC_DIR, "ads.txt"))
