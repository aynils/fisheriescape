# Generated by Django 3.2.2 on 2021-06-17 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trapnet', '0002_remove_sample_water_temp_c'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='water_temp_shore_c',
            new_name='water_temp_c',
        ),
    ]
