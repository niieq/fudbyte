# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-09-21 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_auto_20180921_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
