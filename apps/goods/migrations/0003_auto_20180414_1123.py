# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-14 03:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180414_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '商品', 'verbose_name_plural': '商品'},
        ),
    ]
