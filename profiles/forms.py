from django import forms
from django.forms import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from .models import Profile, City

import string


class LocationField(forms.CharField):

    def clean(self, value):
        if value:
            try:
                city = City.objects.get(name=value)
            except ObjectDoesNotExist:
                allowed = set(string.ascii_letters + '-')
                if set(value) <= allowed:
                    city = City.objects.create(name=value)
                else:
                    raise ValidationError('Wproważ poprawną nazwe miasta')
            return city


class ProfileForm(forms.ModelForm):
    location = LocationField(required=False, widget = forms.widgets.TextInput(
        attrs={
            'hx-get': '/select-location',
            'hx-trigger': 'keyup changed delay:200ms',
            'hx-target': '#location-results',
        })
    )

    class Meta:
        model = Profile
        exclude = ['email_confirmed', 'user', 'slug', 'visited']
        widgets = {
            # 'bio': forms.widgets.Textarea({'autofocus': 'autofocus'}),
            'birth_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
    

