# Generated by Django 3.1.2 on 2021-02-05 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0005_auto_20210205_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_datetime',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_datetime',
        ),
    ]
