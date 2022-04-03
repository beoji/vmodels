from django.contrib import admin
from .models import Profile, Photo


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['profile', 'uploaded_at']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Photo, PhotoAdmin)

