# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 12:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fd', '0004_feedsource_show_on_frontpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedpost',
            name='feed_sources',
        ),
    ]
