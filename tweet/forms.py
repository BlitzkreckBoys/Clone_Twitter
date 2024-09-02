# from django import forms
# from .models import Tweet

# class TweetForm(forms.ModelForm):
#     """Form for creating a new tweet"""
#     class Meta:
#         """Model for tweet"""
#         model = Tweet
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={
#                 'placeholder': 'What’s on your mind?',
#                 'rows': 4,
#                 'class': 'form-control'
#             })
#         }
#         labels = {
#             'content': '',  # Set the label for 'content' to an empty string
#         }
