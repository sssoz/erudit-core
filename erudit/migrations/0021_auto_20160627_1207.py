# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erudit', '0020_thesis_oai_datestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'verbose_name': 'Collection', 'verbose_name_plural': 'Collections'},
        ),
        migrations.AddField(
            model_name='collection',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo'),
        ),
    ]