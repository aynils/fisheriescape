# Generated by Django 2.2.2 on 2019-10-24 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_auto_20191024_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='approver_approval_date',
            new_name='rdg_approval_date',
        ),
    ]
