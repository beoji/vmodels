from django.urls import include, path

from .views import (
    photo_upload_view, 
    photo_detail_view
)

app_name='photos'

urlpatterns = [
    path('upload/', photo_upload_view, name='upload'),
    path('<int:pk>/', photo_detail_view, name='detail'),
]