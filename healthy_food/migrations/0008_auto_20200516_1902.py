# Generated by Django 3.0.4 on 2020-05-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthy_food', '0007_auto_20200516_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='dflt_img.jpg', null=True, upload_to=''),
        ),
    ]
