# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_chatroommember'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatroom',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='chatroommember',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatroommember',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
