from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, DetailView, ListView
from django.contrib import messages
from .models import Profile, Tweet
from .forms import ProfileForm, UserForm, TweetForm

class HomeView(View):
    """ Home view for the profile"""
    def get(self, request, *args, **kwargs):
        """ for the profile view """
        if request.user.is_authenticated:
            tweet_form = TweetForm()
            tweets = Tweet.objects.filter(
                user__in=request.user.profile.follows.values_list('id', flat=True)
            ).order_by('-created_at')
            user_tweets = Tweet.objects.filter(user=request.user)
            tweets = tweets | user_tweets
            tweets = tweets.order_by('-created_at')

            return render(request, 'home.html', {
                'tweet_form': tweet_form,
                'tweets': tweets,
            })
        return redirect('login')
    def post(self, request, *args, **kwargs):
        """ Handle tweet submission """
        if request.user.is_authenticated:
            tweet_form = TweetForm(request.POST, request.FILES)
            if tweet_form.is_valid():
                tweet = tweet_form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                return redirect('home')
        return redirect('login')

class ProfileView(DetailView):
    """Profile view for a specific user"""
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'pk'  # Matches the 'pk' in the URL pattern

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        try:
            profile = Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")
        return profile

class EditProfileView(UpdateView):
    """Edit profile view for the current user"""
    model = Profile
    form_class = ProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)

class FollowingListView(ListView):
    """"List of users"""
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return profile.follows.all()

class FollowersListView(ListView):
    """List of users"""
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Profile.objects.filter(follows=user_profile)

class FollowProfileView(View):
    """Follow or unfollow a user"""
    def post(self, request, *args, **kwargs):
        """for follow and unfollow """
        if request.user.is_authenticated:
            profile_to_follow = get_object_or_404(Profile, pk=kwargs['pk'])
            action = request.POST.get('follow', '')
            if action == 'follow':
                request.user.profile.follows.add(profile_to_follow)
                messages.success(request, 'You are now following this user.')
            elif action == 'unfollow':
                request.user.profile.follows.remove(profile_to_follow)
                messages.success(request, 'You have unfollowed this user.')
            else:
                messages.error(request, 'Invalid action.')
            return redirect('profile', pk=kwargs['pk'])
        return redirect('login')

class ExploreProfileView(ListView):
    """Explore users based on search query"""
    model = Profile
    template_name = 'explore.html'
    context_object_name = 'users'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            return Profile.objects.filter(user__username__icontains=search_query)
        return Profile.objects.all()
