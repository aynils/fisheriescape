# Generated by Django 3.2.14 on 2022-11-16 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herring', '0021_fishdetail_photo_magnification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fishdetail',
            name='photo_magnification',
        ),
        migrations.AddField(
            model_name='fishdetail',
            name='gonad_photo_magnification',
            field=models.FloatField(blank=True, null=True, verbose_name='photo magnification'),
        ),
    ]
