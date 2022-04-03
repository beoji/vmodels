from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from photos.models import Photo
from .choices import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.ForeignKey('City', on_delete=models.SET_NULL, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_photo = models.OneToOneField('photos.Photo', on_delete=models.SET_NULL, blank=True, null=True, related_name='profile_photo')
    profession = models.CharField(max_length=1, choices=PROFESSION)
    experience = models.CharField(max_length=1, choices=EXPERIENCE, blank=True, null=True)
    height = models.PositiveIntegerField(validators=[MinValueValidator(50), MaxValueValidator(260)], blank=True, null=True)
    bust = models.PositiveIntegerField(validators=[MinValueValidator(20), MaxValueValidator(260)], blank=True, null=True)
    waistline = models.PositiveIntegerField(validators=[MinValueValidator(20), MaxValueValidator(260)], blank=True, null=True)
    hips = models.PositiveIntegerField(validators=[MinValueValidator(20), MaxValueValidator(260)], blank=True, null=True)
    hair = models.CharField(max_length=1, choices=HAIR, blank=True, null=True)
    eyes = models.CharField(max_length=1, choices=EYES, blank=True, null=True)
    wear = models.CharField(max_length=1, choices=WEAR, blank=True, null=True)
    shoes = models.PositiveIntegerField(validators=[MinValueValidator(30), MaxValueValidator(60)], blank=True, null=True)
    bra = models.CharField(max_length=1, choices=BRA, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    scope = models.ManyToManyField('ScopeOfWork', related_name='scopes', blank=True)
    visited = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.get_profession_display())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class ScopeOfWork(models.Model):
    scope = models.CharField(max_length=1, choices=SCOPE)


class Region(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class City(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
    
