from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from lazy_crawler.app import config
from lazy_crawler.app.auth import get_current_superuser
from lazy_crawler.app.database import get_session, User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional
from lazy_crawler.app.database.models import ContactSubmission

router = APIRouter(prefix="/admin", tags=["admin"])

# Template Engine
templates = Jinja2Templates(directory=config.TEMPLATES_DIR)


@router.get("/contacts")
async def admin_contacts(
    request: Request,
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_session),
):
    """Admin page to view contact messages"""
    statement = select(ContactSubmission).order_by(ContactSubmission.created_at.desc())
    results = await session.exec(statement)
    contacts = results.all()

    return templates.TemplateResponse(
        "admin_contacts.html",
        {
            "request": request,
            "active_page": "admin_contacts",
            "user": current_user,
            "contacts": contacts,
        },
    )


# Blog Management
from lazy_crawler.app.database.models import BlogPost
from fastapi import Form


@router.get("/blog")
async def admin_blog_list(
    request: Request,
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_session),
):
    """Admin page to list blog posts"""
    statement = select(BlogPost).order_by(BlogPost.created_at.desc())
    results = await session.exec(statement)
    posts = results.all()

    return templates.TemplateResponse(
        "admin_blog.html",
        {
            "request": request,
            "active_page": "admin_blog",
            "user": current_user,
            "posts": posts,
        },
    )


@router.get("/blog/new")
async def admin_blog_new(
    request: Request,
    current_user: User = Depends(get_current_superuser),
):
    """Admin page to create new blog post"""
    return templates.TemplateResponse(
        "admin_blog_form.html",
        {
            "request": request,
            "active_page": "admin_blog",
            "user": current_user,
            "post": None,
        },
    )


@router.post("/blog/new")
async def admin_blog_create(
    request: Request,
    title: str = Form(...),
    slug: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    image_url: Optional[str] = Form(None),
    published: bool = Form(False),
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_session),
):
    """Create new blog post"""
    new_post = BlogPost(
        title=title,
        slug=slug,
        excerpt=excerpt,
        content=content,
        image_url=image_url,
        published=published,
        user_id=current_user.id,
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return RedirectResponse(url="/admin/blog", status_code=303)


@router.get("/blog/{post_id}/edit")
async def admin_blog_edit(
    post_id: int,
    request: Request,
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_session),
):
    """Admin page to edit blog post"""
    post = await session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
        "admin_blog_form.html",
        {
            "request": request,
            "active_page": "admin_blog",
            "user": current_user,
            "post": post,
        },
    )


@router.post("/blog/{post_id}/edit")
async def admin_blog_update(
    post_id: int,
    request: Request,
    title: str = Form(...),
    slug: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    image_url: Optional[str] = Form(None),
    published: bool = Form(False),
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_session),
):
    """Update blog post"""
    post = await session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = title
    post.slug = slug
    post.excerpt = excerpt
    post.content = content
    post.image_url = image_url
    post.published = published

    session.add(post)
    await session.commit()
    return RedirectResponse(url="/admin/blog", status_code=303)


@router.post("/blog/{post_id}/delete")
async def admin_blog_delete(
    post_id: int,
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_session),
):
    """Delete blog post"""
    post = await session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await session.delete(post)
    await session.commit()
    return RedirectResponse(url="/admin/blog", status_code=303)
