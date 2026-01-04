from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from lazy_crawler.app import config
from lazy_crawler.app.auth import get_current_user_optional
from lazy_crawler.app.database import get_session, User, BlogPost
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional
import markdown_it

router = APIRouter(prefix="/blog", tags=["blog"])
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
async def blog_list(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_session),
):
    """List all published blog posts"""
    statement = (
        select(BlogPost)
        .where(BlogPost.published == True)
        .order_by(BlogPost.created_at.desc())
    )
    results = await session.exec(statement)
    posts = results.all()

    return templates.TemplateResponse(
        "blog.html",
        {
            "request": request,
            "active_page": "blog",
            "user": current_user,
            "posts": posts,
        },
    )


@router.get("/{slug}")
async def blog_detail(
    slug: str,
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_session),
):
    """View single blog post"""
    statement = select(BlogPost).where(BlogPost.slug == slug)
    results = await session.exec(statement)
    post = results.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if published OR if user is admin (admins can view drafts)
    if not post.published:
        if not current_user or not current_user.is_superuser:
            raise HTTPException(status_code=404, detail="Post not found")

    # Fetch latest 3 posts for "Related Posts" section (excluding current)
    latest_statement = (
        select(BlogPost)
        .where(BlogPost.published == True, BlogPost.id != post.id)
        .order_by(BlogPost.created_at.desc())
        .limit(3)
    )
    latest_results = await session.exec(latest_statement)
    latest_posts = latest_results.all()

    return templates.TemplateResponse(
        "blog_detail.html",
        {
            "request": request,
            "active_page": "blog",
            "user": current_user,
            "post": post,
            "latest_posts": latest_posts,
        },
    )
