from django.urls import path
from django.conf.urls import url

from .views import *

name_apps = 'hf'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate')
]