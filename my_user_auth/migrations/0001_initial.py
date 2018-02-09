# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('person_id', models.PositiveIntegerField()),
                ('token', models.CharField(max_length=100)),
                ('time_activation', models.DateTimeField()),
                ('user_rating', models.PositiveIntegerField()),
                ('referal_link', models.URLField()),
                ('referer', models.ForeignKey(blank=True, null=True, to='my_user_auth.MyUsers')),
                ('user', models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
