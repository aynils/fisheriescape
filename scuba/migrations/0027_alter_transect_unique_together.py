# Generated by Django 3.2.5 on 2021-12-06 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scuba', '0026_auto_20211206_1148'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transect',
            unique_together={('name', 'region')},
        ),
    ]
