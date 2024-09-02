from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic import View, UpdateView, DetailView, ListView
from django.contrib import messages
from .models import Profile,Tweet
from .forms import ProfileForm, UserForm,TweetForm

class HomeView(View):
    """ Home view for the profile """
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

            # Pagination
            paginator = Paginator(tweets, 10)  # Show 10 tweets per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'home.html', {
                'tweet_form': tweet_form,
                'page_obj': page_obj,
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
        user = get_object_or_404(User, id=user_id)
        return get_object_or_404(Profile, user=user)
class EditProfileView(UpdateView):
    """Edit profile view for the current user"""
    model = Profile
    form_class = ProfileForm
    template_name = 'edit_profile.html'
    paginate_by = 10  # Show 10 profiles per page

    def get_object(self, queryset=None):
        # Retrieve the profile object for the currently logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        # Redirect to the profile page after successful form submission
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        # Add the user form to the context
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        # Save the user form along with the profile form
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
class FollowingTweetsView(ListView):
    """List of tweets from users I follow"""
    model = Tweet
    template_name = 'tweets_list.html'
    context_object_name = 'tweets'

    def get_queryset(self):
        user = self.request.user
        followed_profiles = user.profile.follows.all()  # This returns a QuerySet of Profile objects
        followed_users = User.objects.filter(profile__in=followed_profiles)  # This converts it to a QuerySet of User objects
        return Tweet.objects.filter(user__in=followed_users).order_by('-created_at')
class LikeTweetView(View):
    """Like or unlike a tweet"""
    def post(self, request, tweet_id):
        """for like and unlike """
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return JsonResponse({'error': 'Tweet not found'}, status=404)
        user = request.user
        if user.is_authenticated:
            if user in tweet.likes.all():
                tweet.likes.remove(user)
                liked = False
            else:
                tweet.likes.add(user)
                liked = True
            return JsonResponse({'liked': liked, 'likes_count': tweet.likes.count()})
        return JsonResponse({'error': 'User not authenticated'}, status=401)
class TweetUpdateView(UpdateView):
    """Edit tweet view for the current user"""
    model = Tweet
    form_class = TweetForm
    template_name = 'edit_tweet.html'
    success_url = reverse_lazy('home')  # Redirect to home after successful update

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)  # Ensure users can only edit their own tweets

    def form_valid(self, form):
        
        # You can add additional logic here if needed
        return super().form_valid(form)