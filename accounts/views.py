from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import SignUpForm
from .tokens import account_activation_token


def register_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # current_site = get_current_site(request)
        subject = 'Activate Your Vmodels Account'
        message = render_to_string('registration/activation_email.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        print(message)
        return redirect('activation_sent')
    context = {'form': form}
    template_name = 'registration/register.html'
    return render(request, template_name, context)


def activation_sent(request):
    template_name = 'registration/activation_sent.html'
    return render(request, template_name)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('profile_view')
    else:
        template_name = 'registration/activation_invalid.html'
        return render(request, template_name)
