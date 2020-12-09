from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100, null = True)
    description = models.CharField(max_length=150, null = True)
    text = models.CharField(max_length=500, null = True)
    img = models.ImageField(default="dflt_img.jpg", null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    avatar = models.ImageField(default="dflt_img.jpg", null=True, blank=True)
    me = models.CharField(max_length=255, null = True)

    ADMIN = 1
    MODER = 2
    USER = 3

    ROLE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (MODER, 'MODER'),
        (USER, 'USER'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


class Diet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    energy = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carbohydrate = models.IntegerField()
