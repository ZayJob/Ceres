from django.db import models
from django.contrib.auth.models import User


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
