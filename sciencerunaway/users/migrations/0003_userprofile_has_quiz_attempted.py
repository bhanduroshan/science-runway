# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 06:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='has_quiz_attempted',
            field=models.BooleanField(default=False),
        ),
    ]
