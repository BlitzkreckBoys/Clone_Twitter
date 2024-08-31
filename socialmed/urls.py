from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib import admin
from twitterclone import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('following/', views.following_list, name='following_list'),
    path('followers/', views.followers_list, name='followers_list'),
    path('follow_profile/<int:pk>/', views.follow_profile, name='follow_profile'),
    path('auth/', include('authentication.urls')),
    path('register/', include('registration.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
