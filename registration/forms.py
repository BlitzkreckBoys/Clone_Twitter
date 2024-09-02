from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):
    """Create a new user with additional fields"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True, 
        help_text='Required.',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        help_text='Required.', 
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True, 
        help_text='Required.', 
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    
    class Meta:
        """The name of the new user"""
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
