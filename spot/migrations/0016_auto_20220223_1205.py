# Generated by Django 3.1.2 on 2022-02-23 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0015_auto_20220223_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cu_name',
            field=models.ManyToManyField(blank=True, to='spot.CUName', verbose_name='CU Name'),
        ),
    ]
