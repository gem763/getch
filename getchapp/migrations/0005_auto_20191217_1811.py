# Generated by Django 2.2.7 on 2019-12-17 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('getchapp', '0004_auto_20191217_1753'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='brand',
            unique_together={('id', 'image')},
        ),
    ]