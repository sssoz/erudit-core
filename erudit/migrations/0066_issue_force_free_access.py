# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-20 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erudit', '0065_auto_20170202_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='force_free_access',
            field=models.BooleanField(default=False, verbose_name='Contraindre en libre accès'),
        ),
    ]