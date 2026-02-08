from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@work-email.com'}))

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # We can store full_name in first_name/last_name or a custom field if it existed.
        # Since User is AbstractUser, it has first_name and last_name.
        # Let's split full_name into first and last name for standard Django fields
        names = self.cleaned_data['full_name'].split(' ', 1)
        user.first_name = names[0]
        if len(names) > 1:
            user.last_name = names[1]

        if commit:
            user.save()
        return user
