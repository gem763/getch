# Generated by Django 2.2.7 on 2020-01-20 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getchapp', '0005_auto_20200119_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='num_vote_down',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='num_vote_up',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='vote_score',
        ),
        migrations.AddField(
            model_name='user',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='users_bookmarked', to='getchapp.Channel'),
        ),
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='users_liked', to='getchapp.Channel'),
        ),
    ]
