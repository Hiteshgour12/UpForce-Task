# Generated by Django 4.2.2 on 2023-06-28 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_remove_like_likes_post_liked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='likes',
            field=models.ManyToManyField(related_name='blogpost_like', to='post.post'),
        ),
    ]