from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    """User login form"""
    class Meta:
        """The name of the form"""
        model = AuthenticationForm
        fields = ['username', 'password']
