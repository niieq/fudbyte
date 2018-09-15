# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-09-15 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='food',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.datetime_safe.datetime.today),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='slug',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.datetime_safe.datetime.today),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='slug',
            field=django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, null=True),
        ),
    ]
