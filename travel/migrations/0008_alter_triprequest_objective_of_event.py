# Generated by Django 3.2 on 2021-05-19 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_auto_20210511_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='objective_of_event',
            field=models.TextField(blank=True, null=True, verbose_name='what is the objective of this activity (conference, meeting, fieldwork)?'),
        ),
    ]
