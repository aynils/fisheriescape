# Generated by Django 2.0.4 on 2018-09-05 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herring', '0012_auto_20180905_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='district',
            old_name='province',
            new_name='province_id',
        ),
    ]
