# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-01-19 14:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_darksidersindex'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DarkSidersIndex',
        ),
    ]