# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-05-27 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('hostname', models.CharField(db_index=True, max_length=32, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(db_index=True)),
                ('port', models.IntegerField()),
                ('b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Business')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=18)),
                ('type', models.CharField(max_length=18)),
                ('ctime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='r',
            field=models.ManyToManyField(to='app01.Host'),
        ),
    ]
