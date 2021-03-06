# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-06 12:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0004_auto_20151206_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id_review', models.AutoField(primary_key=True, serialize=False)),
                ('opinion', models.CharField(max_length=140)),
                ('rating', models.CharField(choices=[('1', 'Very poor'), ('2', 'Poor'), ('3', 'Not bad'), ('4', 'Good'), ('5', 'Very Good')], max_length=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
