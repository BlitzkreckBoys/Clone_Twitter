from django import forms
from django.contrib.auth.models import User
from .models import Profile,Tweet
class ProfileForm(forms.ModelForm):
    """Form for editing user profile information"""
    class Meta:
        """model for profile"""
        model = Profile
        fields = ['bio', 'profile_picture','date_of_birth']
class UserForm(forms.ModelForm):
    """Form for editing user information"""
    class Meta:
        """model for user"""
        model = User
        fields = ['username', 'email']
class TweetForm(forms.ModelForm):
    """Form for creating a new tweet"""
    class Meta:
        """model for tweet"""
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'What’s on your mind?',
                'rows': 4,
                'class': 'form-control'
            })
        }
