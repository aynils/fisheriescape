# Generated by Django 2.1.4 on 2019-04-16 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ios2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mooring',
            name='orientation',
        ),
        migrations.AddField(
            model_name='instrumentmooring',
            name='orientation',
            field=models.TextField(blank=True, null=True, verbose_name='Orientation'),
        ),
    ]
