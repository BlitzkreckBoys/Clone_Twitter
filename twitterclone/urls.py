from django.urls import path
from .views import HomeView, ProfileView, EditProfileView, FollowingListView, FollowersListView, FollowProfileView, ExploreProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('following/', FollowingListView.as_view(), name='following_list'),
    path('followers/', FollowersListView.as_view(), name='followers_list'),
    path('follow_profile/<int:pk>/', FollowProfileView.as_view(), name='follow_profile'),
    path('explore/', ExploreProfileView.as_view(), name='explore_profile'),
]
