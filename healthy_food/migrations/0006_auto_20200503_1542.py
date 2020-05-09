# Generated by Django 3.0.4 on 2020-05-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthy_food', '0005_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'ADMIN'), (2, 'MODER'), (3, 'USER')], null=True),
        ),
    ]