from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import SignupForm

class SignupView(FormView):
    """User registration view"""
    form_class = SignupForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')  # Redirect URL after successful form submission

    def form_valid(self, form):
        user = form.save()
        # Optionally, you can send a welcome email here or perform other actions
        messages.success(self.request, 'Your account has been created successfully! You can now log in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
