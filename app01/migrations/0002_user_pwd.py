# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-05-27 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pwd',
            field=models.CharField(default=11, max_length=32),
            preserve_default=False,
        ),
    ]
