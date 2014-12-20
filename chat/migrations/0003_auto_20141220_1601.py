# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('chat', '0002_chat_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(to='chat.MyUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='user_id',
            field=models.ForeignKey(to='chat.MyUser'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
