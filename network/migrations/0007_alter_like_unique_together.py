# Generated by Django 5.0.6 on 2024-06-06 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_remove_post_likes_like_post_likes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('post', 'user')},
        ),
    ]
