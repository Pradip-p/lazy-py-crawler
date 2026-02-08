from django.contrib import admin
from django.utils.html import format_html
from .models import User, DatasetMetadata, ContactSubmission, BlogPost, Project

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'provider', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'provider', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'last_login', 'date_joined')
    ordering = ('-created_at',)

    fieldsets = (
        ('Account Information', {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Authentication', {
            'fields': ('provider', 'last_login', 'date_joined', 'created_at')
        }),
    )

@admin.register(DatasetMetadata)
class DatasetMetadataAdmin(admin.ModelAdmin):
    list_display = ('filename', 'file_type', 'formatted_file_size', 'user', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('filename', 'sync_id', 'mongo_collection_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def formatted_file_size(self, obj):
        """Display file size in human-readable format"""
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    formatted_file_size.short_description = 'File Size'

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def message_preview(self, obj):
        """Show first 50 characters of message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'user', 'created_at', 'preview_link')
    readonly_fields = ('slug', 'created_at', 'preview_link')
    search_fields = ('title', 'content', 'excerpt')
    list_filter = ('published', 'created_at', 'user')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'image_url', 'published', 'user')
        }),
        ('Blog Content', {
            'fields': ('content',),
            'classes': ('extrapretty',),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def preview_link(self, obj):
        if obj.slug:
            return format_html('<a href="/blog/{}" target="_blank">View Post</a>', obj.slug)
        return ""
    preview_link.short_description = "Preview"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'data_type', 'output_format', 'project_type', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'project_type', 'data_type', 'output_format', 'created_at')
    search_fields = ('name', 'description', 'urls')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Project Information', {
            'fields': ('user', 'name', 'description')
        }),
        ('Configuration', {
            'fields': ('data_type', 'output_format', 'project_type', 'status')
        }),
        ('URLs & Data', {
            'fields': ('urls', 'mongo_collection'),
            'classes': ('wide',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

# Admin Site Header Customization
admin.site.site_header = "Crawlio Administration"
admin.site.site_title = "Crawlio Admin Portal"
admin.site.index_title = "Welcome to Crawlio Management Dashboard"
