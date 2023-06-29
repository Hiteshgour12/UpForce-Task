# Generated by Django 4.2.2 on 2023-06-28 10:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_remove_like_likes_alter_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='likes',
            field=models.ManyToManyField(related_name='blogpost_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
