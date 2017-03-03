# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 13:40
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170303_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='common_answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='other_answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='signup_type',
            field=models.IntegerField(choices=[(1, 'Girls'), (2, 'Role Model')], default=1, verbose_name='User Type'),
        ),
    ]
