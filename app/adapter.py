from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """
        Redirect superusers to admin panel, normal users to dashboard.
        """
        user = request.user
        if user.is_superuser:
            return '/admin/'
        return reverse('dashboard')
