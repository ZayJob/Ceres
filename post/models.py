from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, null = True)
    description = models.CharField(max_length=150, null = True)
    text = models.CharField(max_length=500, null = True)
    img = models.ImageField(default="dflt_img.jpg", null=True, blank=True)