from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PhotoForm
from .models import Photo


@login_required
def photo_upload_view(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.profile = request.user.profile
            obj.save()
            return redirect('profile_view')
        else:
            return render(request, 'photos/upload.html', {'form': form})
    else:
        form = PhotoForm()
    return render(request, 'photos/upload.html', {'form': form})


def photo_detail_view(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.visited = F('visited') + 1
    photo.save()
    photo.refresh_from_db()
    context = {'photo': photo}
    return render(request, 'photos/detail.html', context=context)
