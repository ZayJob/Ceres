from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    pass


class Diet(models.Model):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
