# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-22 14:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pwmanager', '0006_auto_20170621_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendingdevicerequest',
            name='verified',
        ),
    ]