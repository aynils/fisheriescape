# Generated by Django 3.2.14 on 2022-11-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herring', '0020_species_use_fmb'),
    ]

    operations = [
        migrations.AddField(
            model_name='fishdetail',
            name='photo_magnification',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='photo magnification'),
        ),
    ]
