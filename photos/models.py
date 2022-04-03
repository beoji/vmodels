from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .utils import make_thumbnail

import uuid
import os


def photo_directory_path(instance, filename):
    new_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    return '{0}/{1}'.format(instance.profile.user.username, new_filename)


class Photo(models.Model):
    GENRE = (
        ('A', 'Fashion'),
        ('B', 'Portret'),
        ('C', 'Glamour'),
    )
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=photo_directory_path, height_field='height', width_field='width')
    thumbnail = models.ImageField(height_field='height', width_field='width', null=True)
    height=models.PositiveIntegerField()
    width=models.PositiveIntegerField()
    description = models.TextField(max_length=500, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=1, choices=GENRE)
    visited = models.PositiveIntegerField(default=0)

    def photo_filename(self):
        return os.path.basename(self.photo.name)


def save_thumbnail(sender, instance, created, **kwargs):
    if created:
        post_save.disconnect(save_thumbnail, sender=sender)

        thumbnail = make_thumbnail(instance)
        new_filename = instance.profile.user.username\
        + '/' + os.path.splitext(instance.photo_filename())[0]\
        + '_thumbnail' + os.path.splitext(instance.photo_filename())[1]

        instance.thumbnail.save(new_filename, InMemoryUploadedFile(
            thumbnail,          # file
            None,               # field_name
            new_filename,       # file name
            'image/jpeg',       # content_type
            thumbnail.tell,     # size
            None)               # content_type_extra
        )

        post_save.connect(save_thumbnail, sender=sender)

post_save.connect(save_thumbnail, sender=Photo)
