# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-09-18 12:40
from __future__ import unicode_literals

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.user_profile_image),
        ),
    ]
