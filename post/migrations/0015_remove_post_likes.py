# Generated by Django 4.2.2 on 2023-06-29 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0014_alter_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]