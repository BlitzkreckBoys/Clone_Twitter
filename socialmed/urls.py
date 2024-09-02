from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('twitter_clone.urls')),  # Note the trailing slash
    path('auth/', include('authentication.urls')),
    path('register/', include('registration.urls')),
    # path('', include('tweet.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
