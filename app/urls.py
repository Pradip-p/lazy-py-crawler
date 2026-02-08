from django.urls import path
from . import views
from .upload_views import custom_upload_file

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('faq/', views.faq_redirect, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('company/', views.company, name='company'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/logout/', views.logout_view, name='auth_logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', custom_upload_file, name='custom_upload_file'),  # CKEditor upload
]
