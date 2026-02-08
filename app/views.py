from django.shortcuts import render, redirect
from django.views import View
from .models import BlogPost, ContactSubmission
from django.core.paginator import Paginator

def index(request):
    latest_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]
    return render(request, 'index.html', {
        'latest_posts': latest_posts,
        'active_page': 'home'
    })

def about(request):
    return render(request, 'about.html', {'active_page': 'about'})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        import json
        from django.http import JsonResponse
        try:
            data = json.loads(request.body)
            ContactSubmission.objects.create(
                full_name=data.get('full_name'),
                email=data.get('email'),
                message=data.get('message')
            )
            return JsonResponse({'message': 'Thank you! Your message has been received.'}, status=200)
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=400)
    return render(request, 'app/contact.html', {'active_page': 'contact'})

def pricing(request):
    return render(request, 'pricing.html', {'active_page': 'pricing'})

def faq_redirect(request):
    return redirect('/pricing#faq')

def privacy(request):
    return render(request, 'privacy.html', {'active_page': 'privacy'})

def company(request):
    # Data from FastAPI pages.py
    team_members = [
        {"name": "Tilak Pathak", "role": "Founder & CEO", "image": "https://ui-avatars.com/api/?name=Tilak+Pathak&background=4a154b&color=fff"},
        {"name": "Sarah Chen", "role": "CTO", "image": "https://ui-avatars.com/api/?name=Sarah+Chen&background=1264a3&color=fff"},
        {"name": "James Wilson", "role": "Head of Product", "image": "https://ui-avatars.com/api/?name=James+Wilson&background=2eb67d&color=fff"},
        {"name": "Emily Rodriguez", "role": "VP of Sales", "image": "https://ui-avatars.com/api/?name=Emily+R&background=e01e5a&color=fff"},
        {"name": "Emily Wilson", "role": "Data aquistion Lead", "image": "https://ui-avatars.com/api/?name=Emily+Wilson&background=2eb67d&color=fff"},
        {"name": "William Lee", "role": "Lead Data Scientist", "image": "https://ui-avatars.com/api/?name=William+Lee&background=e01e5a&color=fff"},
    ]
    job_openings = [
        {"title": "Senior Python Engineer", "department": "Engineering", "location": "Remote (Global)", "tags": ["Full-time", "Senior"]},
        {"title": "Data Solutions Architect", "department": "Solutions", "location": "Sydney / Remote", "tags": ["Full-time", "Mid-Senior"]},
        {"title": "Product Designer (UI/UX)", "department": "Design", "location": "New York / Remote", "tags": ["Contract", "Mid-Level"]},
    ]
    return render(request, 'company.html', {
        'active_page': 'company',
        'team_members': team_members,
        'job_openings': job_openings
    })

def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj, 'posts': page_obj, 'active_page': 'blog'})

def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug)
    return render(request, 'blog_detail.html', {'post': post, 'active_page': 'blog'})

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from app.forms import UserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify backend explicitly when multiple backends are configured
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Redirect superusers to admin, normal users to dashboard
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect superusers to admin, normal users to dashboard
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'active_page': 'dashboard'})
