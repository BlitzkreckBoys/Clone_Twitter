from django.contrib.auth.models import User
from django import forms
from .models import Profile, Tweet


class ProfileForm(forms.ModelForm):
    """Form for editing user profile information"""
    class Meta:
        """Model for profile"""
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture', 'date_of_birth']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }       
class UserForm(forms.ModelForm):
    """Form for editing user information"""
    class Meta:
        """Model for user"""
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class TweetForm(forms.ModelForm):
    """Form for creating a new tweet"""
    class Meta:
        """Model for tweet"""
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'What’s on your mind?',
                'rows': 4,
                'class': 'form-control'
            })
        }
        labels = {
            'content': '',  # Set the label for 'content' to an empty string
        }
