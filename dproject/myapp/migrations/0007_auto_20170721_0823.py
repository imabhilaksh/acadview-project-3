# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 02:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_upvotemodel_has_upvote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upvotemodel',
            name='has_upvote',
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='has_upvote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='comment_text',
            field=models.CharField(max_length=500),
        ),
    ]