from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from autoslug import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True)
    provider = models.CharField(max_length=50, default="email")  # "email" or "google"
    profile_picture = models.URLField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class DatasetMetadata(models.Model):
    sync_id = models.CharField(max_length=255, unique=True, db_index=True)
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField()
    mongo_collection_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.filename

class ContactSubmission(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "contact_us"

    def __str__(self):
        return f"{self.full_name} - {self.email}"

class BlogPost(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    content = CKEditor5Field(config_name='extends')  # Rich text content with CKEditor 5
    excerpt = models.CharField(max_length=500)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "blog_posts"

    def __str__(self):
        return self.title

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    data_type = models.CharField(max_length=100, default="Generic")  # E-commerce, Real Estate, etc.
    output_format = models.CharField(max_length=50, default="CSV")  # CSV, JSON, Excel
    project_type = models.CharField(max_length=50, default="One-time")  # One-time, Recurring
    urls = models.TextField()  # Comma-separated or multi-line URLs
    status = models.CharField(max_length=50, default="Pending")  # Pending, Processing, Completed, Failed
    mongo_collection = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
