# Generated by Django 3.2.4 on 2021-10-04 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csas2', '0043_auto_20211004_1025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processcost',
            old_name='meeting',
            new_name='process',
        ),
    ]
