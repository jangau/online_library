# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-06 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image_height',
            field=models.PositiveIntegerField(blank=True, default='100', editable=False, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='image_width',
            field=models.PositiveIntegerField(blank=True, default='100', editable=False, null=True),
        ),
    ]
