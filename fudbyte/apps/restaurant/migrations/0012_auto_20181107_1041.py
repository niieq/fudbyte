# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-11-07 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_auto_20181107_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantuser',
            name='role',
            field=models.CharField(blank=True, choices=[('Owner', 'Owner'), ('Admin', 'Admin'), ('Following', 'Following')], max_length=255, null=True),
        ),
    ]
