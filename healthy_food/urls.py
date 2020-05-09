from django.urls import path
from django.conf.urls import url

from .views import *

name_apps = 'hf'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('profile/', profile, name='profile'),
    path('calculator/', calculator, name='calculator'),
    path('diets/', diets, name='diets'),
    path('search_food/', search_food, name='s_food'),
    path('create_post/', create_post, name='c_post'),
]