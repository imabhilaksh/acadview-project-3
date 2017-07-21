# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 05:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sessiontoken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.UserModel')),
            ],
        ),
    ]
