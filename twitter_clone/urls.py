from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tweets_list/', FollowingTweetsView.as_view(), name='tweets_list'),
    path('like_tweet/<int:tweet_id>/', LikeTweetView.as_view(), name='like_tweet'),
    path('edit_tweet/<int:pk>/', TweetUpdateView.as_view(), name='edit_tweet'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('following/', FollowingListView.as_view(), name='following_list'),
    path('followers/', FollowersListView.as_view(), name='followers_list'),
    path('follow_profile/<int:pk>/', FollowProfileView.as_view(), name='follow_profile'),
    path('explore/', ExploreProfileView.as_view(), name='explore_profile'),

]
