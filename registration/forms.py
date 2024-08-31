from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class SignupForm(UserCreationForm):
    """Create a new user"""
    class Meta:
        """ The name of the new user"""
        model = User
        fields = ['username', 'password1', 'password2']
