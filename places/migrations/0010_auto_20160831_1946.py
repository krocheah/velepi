# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_auto_20160825_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='vote',
            field=models.IntegerField(choices=[(1, 'Bad'), (2, 'Not Bad'), (3, 'Meh'), (4, 'Fine'), (5, 'Rocks')], default=3),
        ),
    ]