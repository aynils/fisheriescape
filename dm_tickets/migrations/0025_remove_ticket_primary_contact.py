# Generated by Django 2.1.4 on 2019-03-21 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dm_tickets', '0024_ticket_primary_contact1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='primary_contact',
        ),
    ]
