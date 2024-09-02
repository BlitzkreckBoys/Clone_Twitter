from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('twitterclone.urls')),  # Include URLs from the twitterclone app
    path('auth/', include('authentication.urls')),  # Include URLs from the authentication app
    path('register/', include('registration.urls')),  # Include URLs from the registration app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
