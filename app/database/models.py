from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: Optional[str] = Field(default=None)
    full_name: Optional[str] = None
    provider: str = Field(default="email")  # "email" or "google"
    profile_picture: Optional[str] = None
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DatasetMetadata(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sync_id: str = Field(index=True, unique=True)
    filename: str
    file_type: str
    file_size: int
    mongo_collection_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class ContactSubmission(SQLModel, table=True):
    __tablename__ = "contact_us"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(index=True)
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BlogPost(SQLModel, table=True):
    __tablename__ = "blog_posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(index=True, unique=True)
    content: str  # Markdown or HTML content
    excerpt: str = Field(max_length=500)
    image_url: Optional[str] = None
    published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(index=True)
    description: Optional[str] = None
    data_type: str = Field(default="Generic")  # E-commerce, Real Estate, etc.
    output_format: str = Field(default="CSV")  # CSV, JSON, Excel
    project_type: str = Field(default="One-time")  # One-time, Recurring
    urls: str  # Comma-separated or multi-line URLs
    status: str = Field(default="Pending")  # Pending, Processing, Completed, Failed
    mongo_collection: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
