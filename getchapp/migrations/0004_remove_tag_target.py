# Generated by Django 2.2.7 on 2020-01-08 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('getchapp', '0003_post_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='target',
        ),
    ]
