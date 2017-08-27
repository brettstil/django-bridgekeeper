# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 20:42
from __future__ import unicode_literals

import bridgekeeper.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('code', models.CharField(db_index=True, default=bridgekeeper.models.generate_code, max_length=255, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='code')),
                ('expired', models.DateTimeField(blank=True, help_text='Invite not valid after expired datetime', null=True, verbose_name='expired')),
                ('user', models.ForeignKey(blank=True, help_text='Invite creator', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
