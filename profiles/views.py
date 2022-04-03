from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from photos.models import Photo

from .forms import ProfileForm
from .models import Profile, City


def home_view(request):
    profile_list = Profile.objects.all()
    context = {
        'profile_list': profile_list,
    }
    return render(request, 'home.html', context=context)


@login_required
def profile_view(request):
    return render(request, 'profiles/settings.html')


def profile_detail_view(request, slug):
    profile = Profile.objects.get(slug=slug)
    # Checking if profile belongs to logged user, it will be used in template
    is_my_profile = request.user.is_authenticated & (request.user == profile.user)
    context = {
        'profile': profile,
        'is_my_profile': is_my_profile
    }
    template_name = 'profiles/detail.html'
    return render(request, template_name, context)


class ProfileDetailView(DetailView):
    
    model = Profile
    context_object_name = 'profile'
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile']
        is_auth = self.request.user.is_authenticated
        is_my = self.request.user == profile.user
        context['is_my_profile'] = is_auth & is_my      # Checking if profile belongs to logged user
        return context
    
    
@login_required
def profile_update_view(request):
    template_name = 'profiles/update.html'
    user = request.user
    profile = Profile.objects.get(user__id=user.id)
    if request.method == 'GET':
        initial = {}
        if profile.location:
            initial = {'location': profile.location.name}
        form = ProfileForm(instance=profile, initial=initial)
    else:
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            return redirect('profile_view')
    context = {'form': form}
    return render(request, template_name, context=context)


def select_location_hx(request):
    if request.htmx:
        if not request.GET.get('location') or len(request.GET.get('location')) < 2:
            context = {'locations': None}
        elif request.GET.get('location'):
            q = request.GET.get('location')
            qs = City.objects.filter(name__istartswith=q)
            context = {'locations': qs}
        return render(request, 'profiles/snippets/select_location.html', context)
        