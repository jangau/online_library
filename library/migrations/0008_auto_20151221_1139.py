# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_book_iban'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='IBAN',
            new_name='ISBN',
        ),
    ]
