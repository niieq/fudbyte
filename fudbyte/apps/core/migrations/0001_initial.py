# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-09-21 23:11
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataScrap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.ShortUUIDField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('source', models.CharField(blank=True, choices=[('jumia_food', 'Jumia Food')], max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
