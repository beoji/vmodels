from django.urls import include, path

from .views import (
    register_view,
    activation_sent,
    activate,
)

# app_name='accounts'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_view, name='register'),
    path('activation_sent/', activation_sent, name='activation_sent'),
    path('activate/<uidb64>/<token>/', activate, name='activate')
]