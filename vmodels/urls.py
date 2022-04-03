from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from profiles.views import (
    home_view, 
    profile_view,
    select_location_hx
)

urlpatterns = [
    path('', home_view, name='home_view'),
    path('', include('accounts.urls')),
    path('profile/', profile_view, name='profile_view'),
    path('profiles/', include('profiles.urls')),
    path('photos/', include('photos.urls')),
    path('admin/', admin.site.urls),
    path('select-location/', select_location_hx, name='select-location'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
