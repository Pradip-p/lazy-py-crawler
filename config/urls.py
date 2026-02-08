from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Also explicitly add STATICFILES_DIRS for development if needed,
    # though standard static() usually handles STATIC_ROOT/STATIC_URL
    # In development with DEBUG=True, Django handles STATICFILES_DIRS automatically.
