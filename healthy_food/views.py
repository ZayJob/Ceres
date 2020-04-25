from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import transaction

from .models import Profile
from .tokens import account_activation_token
from .forms import SignupForm, ProfileForm, LoginForm


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile(
                url=signup_form.changed_data["url"],
                company=signup_form.changed_data["company"],
                phone=signup_form.changed_data["phone"],
                address=signup_form.changed_data["address"],
                avatar=signup_form.changed_data["avatar"],
                user=user
            )
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account/email_message.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = signup_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'account/confirm_email.html')
    else:
        signup_form = SignupForm()
        profile_form = ProfileForm()
    return render(request, 'account/signup.html', {'signup_form': signup_form, 'profile_form': profile_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        request.session['user_id'] = uid
        return render(request, 'account/confirmation.html')
    else:
        return render(request, 'account/activation_invalid.html')


def home(request):
    try:
        request.session['user_id']
        return render(request, 'home/home.html', context={'user_login': True})
    except KeyError:
        return render(request, 'home/home.html', context={'user_login': False})


def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            try:
                user = User.objects.get(username=request.POST.get("username"), password=request.POST.get("password"))
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.pk
        return render(request, 'home/home.html', context={'user_login': True})
    else:
        login_form = LoginForm()
    return render(request, 'account/login.html', {'login_form': login_form})


def logout_user(request):
    logout(request)
    request.session['user_id'] = False
    return render(request, 'account/logout.html')