from django.contrib import admin
from django.utils.html import format_html
from .models import User, DatasetMetadata, ContactSubmission, BlogPost, Project

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(DatasetMetadata)
class DatasetMetadataAdmin(admin.ModelAdmin):
    list_display = ('filename', 'file_type', 'file_size', 'created_at')
    search_fields = ('filename', 'sync_id')

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created_at')
    search_fields = ('full_name', 'email')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'created_at', 'preview_link')
    readonly_fields = ('slug', 'preview_link')
    search_fields = ('title', 'content')
    list_filter = ('published', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt', 'image_url', 'published', 'user')
        }),
        ('Blog Content', {
            'fields': ('content',),
            'classes': ('extrapretty',),
        }),
    )

    def preview_link(self, obj):
        if obj.slug:
            return format_html('<a href="/blog/{}" target="_blank">View Post</a>', obj.slug)
        return ""
    preview_link.short_description = "Preview"

# Admin Site Header Customization
admin.site.site_header = "Crawlio Administration"
admin.site.site_title = "Crawlio Admin Portal"
admin.site.index_title = "Welcome to Crawlio Management Dashboard"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'created_at')
    list_filter = ('status', 'project_type', 'data_type')
    search_fields = ('name', 'description')
