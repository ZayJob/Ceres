from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from .views import *

name_apps = 'hf'

urlpatterns = [
    path('', home),
    path('signup', signup_post),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('logout', logout_user),
    path('login', login_user_post),
    path('profile', profile),
    path('calculator', calculator_post),
    path('search_food', search_food_post),
    path('create_post', create_post_post),
    path('render_page', render_page),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)