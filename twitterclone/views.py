from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ProfileForm, UserForm, TweetForm
from .models import Profile,Tweet

def home(request):
    """ Return the home page and tweets for the current user"""
    if request.user.is_authenticated:
        # Handle the tweet form submission
        if request.method == "POST":
            tweet_form = TweetForm(request.POST)
            if tweet_form.is_valid():
                tweet = tweet_form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, 'Tweet posted successfully.')
            else:
                messages.error(request, 'Error posting tweet.')

        # Initialize the tweet form
        tweet_form = TweetForm()

        # Get the user's tweets and tweets from followed users
        tweets = Tweet.objects.filter(
            user__in=request.user.profile.follows.values_list('id', flat=True)
        ).order_by('-created_at')

        # Include the user's own tweets
        user_tweets = Tweet.objects.filter(user=request.user)
        tweets = tweets | user_tweets
        tweets = tweets.order_by('-created_at')

        return render(request, 'home.html', {
            'tweet_form': tweet_form,
            'tweets': tweets,
        })
    else:
        return redirect('login')

            
    # If the user is not authenticated, just show the title
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)
    return render(request, 'profile.html', {'profile': user_profile})
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user) 
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, files=request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)   
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            # Redirect to the profile page using the user's id
            return redirect('profile', user_id=request.user.id)
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'user_form': user_form
    })
def following_list(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        following_profiles = profile.follows.all()
        return render(request, 'profile_list.html', {
            'title': 'Following',
            'users': following_profiles
        })    
    else:
        return redirect('login')
def followers_list(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
        followers_profiles = Profile.objects.filter(follows=user_profile)
        return render(request, 'profile_list.html', {
            'title': 'Followers',
            'users': followers_profiles  # Passing profiles to the template
        })
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('login')
def follow_profile(request,pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, pk=pk)
        if request.method == "POST":
            current_user_profile = request.user.profile
            actiont = request.POST['follow']
            if actiont == 'follow':
                current_user_profile.follows.add(profile)
            elif actiont == 'unfollow':
                current_user_profile.follows.remove(profile)
            # current_user_profile.save()
            return redirect('profile', pk=pk)
        else:
            return render(request, 'profile.html', {'profile': profile})
def explore_profile(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all()
        return render(request, 'profile_list.html', {
            'title': 'Explore',
            'users': profiles
        })
    else:
        return redirect('login')