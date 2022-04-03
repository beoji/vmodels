from django.urls import path

from .views import (
    profile_view,
    profile_update_view,
    ProfileDetailView,
    profile_detail_view,
    select_location_hx
)

app_name='profiles'

urlpatterns = [
    path('settings/', profile_view, name='settings'),
    path('update/', profile_update_view, name='update'),
    path('<slug:slug>/', profile_detail_view, name='detail'),
]