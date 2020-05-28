from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import transaction

import requests as req
import json

from .models import Profile, Post
from .tokens import account_activation_token
from .forms import SignupForm, ProfileForm, LoginForm


@transaction.atomic
def signup_post(request):
    try:
        user = User(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password1'),
        )
        user.is_active = True
        user.save()
        profile = Profile(
            url=request.POST.get("url"),
            company=request.POST.get("company"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            me="",
            user=user
        )
        profile.save()
        
        #current_site = get_current_site(request)
        #mail_subject = 'Activate your blog account.'
        #message = render_to_string('account/email_message.html', {
        #    'user': user,
        #    'domain': current_site.domain,
        #    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #    'token': account_activation_token.make_token(user),
        #})
        #to_email = request.POST.get('email')
        #email = EmailMessage(mail_subject, message, to=[to_email])
        #email.send()

        signup_form = SignupForm()
        profile_form = ProfileForm()
        return render(request, 'signup.html', context={'signup_form': signup_form, 'profile_form': profile_form})
    except Exception:
        return JsonResponse({"success" : "no"})


def signup(request):
    signup_form = SignupForm()
    profile_form = ProfileForm()
    return {'signup_form': signup_form, 'profile_form': profile_form}


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
        return None
    else:
        return None


def home(request):
    try:
        request.session['user_id']
        return render(request, 'base_template.html')
    except KeyError:
        return render(request, 'base_template.html')

def login_user_post(request):
    try:
        user = User.objects.get(username=request.POST.get("username"), password=request.POST.get("password"))
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        login(request, user)
        request.session['user_id'] = user.pk
        login_form = LoginForm()
        return render(request, "login.html", context={'login_form': login_form})
    return HttpResponse("no")

def login_user(request):
    login_form = LoginForm()
    return {'login_form': login_form}


def logout_user(request):
    logout(request)
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return render(request, 'home.html')

def profile(request):
    try:
        request.session['user_id']
        try:
            user = User.objects.get(pk=request.session['user_id'])
            profile = Profile.objects.get(user_id=request.session['user_id'])
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            profile = None
        if user != None and profile != None:
            return render(request, "profile.html", context={'user': user, 'profile': profile})
    except KeyError:
        return HttpResponse("no")

def diets(request):
    try:
        posts = Post.objects.all()
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        posts = None
    if posts != None:
        try:
            request.session['user_id']
            return {'posts': posts[len(posts) - 3:len(posts)]}
        except KeyError:
            return {'posts': posts[len(posts) - 3:len(posts)]}

def create_post_post(request):
    post = Post(
        title=request.POST.get("title"),
        description=request.POST.get("description"),
        text=request.POST.get('create-post-body-text'),
    )
    post.save()
    return render(request, 'create_post.html')

def create_post(request):
    return None

def search_food_post(request):
    respons = req.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=EVuhK3UbNku53YdTuw044oAUBsIJF0fGDpRhwKhG&query={0}'.format(request.POST.get('data')))
    data = json.loads(respons.text)
    answer = []
    for item in data['foods']:
        answer.append({'name': item['description']})
        for info in item['foodNutrients']:
            if info["nutrientNumber"] == '205':
                answer[-1]['carbohydrate'] = info['value']
            if info["nutrientNumber"] == '208':
                answer[-1]['energy'] = info['value']
            if info["nutrientNumber"] == '204':
                answer[-1]['fat'] = info['value']
            if info["nutrientNumber"] == '203':
                answer[-1]['protein'] = info['value']
    return render(request, "search_food.html", context={'answer': answer[:10]})

def search_food(request):
    try:
        request.session['user_id']
        return None
    except KeyError:
        return None

def calculator_post(request):
    if request.POST.get('male') == "on":
        BMR = 88.362 + 13.397 * int(request.POST.get('weight')) + 4.799 * int(request.POST.get('height')) - 5.677 * int(request.POST.get('age'))
    elif request.POST.get('female') == "on":
        BMR = 447.593 + 9.247 * int(request.POST.get('weight')) + 3.098 * int(request.POST.get('height')) - 4.330 * int(request.POST.get('age'))

    if request.POST.get('activ') == 'Сидячий образ жизни':
        AMR = 1.2
    elif request.POST.get('activ') == 'Умеренная активность (легкие физические нагрузки либо занятия 1-3 раз в неделю)':
        AMR = 1.375
    elif request.POST.get('activ') == 'Средняя активность (занятия 3-5 раз в неделю)':
        AMR = 1.55
    elif request.POST.get('activ') == 'Активные люди (интенсивные нагрузки, занятия 6-7 раз в неделю)':
        AMR = 1.725
    elif request.POST.get('activ') == 'Спортсмены и люди, выполняющие сходные нагрузки (6-7 раз в неделю)':
        AMR = 1.9

    energy = int(BMR * AMR)
    protein = int(energy * 0.3 / 4)
    fat = int(energy * 0.1 / 9)
    carbohydrate = int(energy * 0.6 / 4)

    return render(request, "calculator.html", context={'energy':energy, 'protein':protein, 'fat':fat, 'carbohydrate':carbohydrate})

def calculator(request):
    try:
        request.session['user_id']
        return None
    except KeyError:
        return None

def render_page(request):
    if request.GET['page'] == 'diets':
        cont = diets(request)
    elif request.GET['page'] == 'login':
        cont = login_user(request)
    elif request.GET['page'] == 'search_food':
        cont = search_food(request)
    elif request.GET['page'] == 'calculator':
        cont = calculator(request)
    elif request.GET['page'] == 'signup':
        cont = signup(request)
    elif request.GET['page'] == 'create_post':
        cont = create_post(request)
    else:
        cont = None
    return render(request, "{0}.html".format(request.GET['page']), context=cont)