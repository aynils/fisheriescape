# Generated by Django 3.2.15 on 2022-12-22 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacificsalmondatahub', '0012_auto_20221221_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acronym',
            old_name='acronym',
            new_name='acronym_Letters',
        ),
    ]
