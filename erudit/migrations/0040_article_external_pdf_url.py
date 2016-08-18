# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-18 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erudit', '0039_journal_website_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='external_pdf_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL PDF'),
        ),
    ]
