# Generated by Django 2.1.4 on 2019-03-28 16:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0014_auto_20190328_0752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crab',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='gcsample',
            options={'ordering': ['traps_set', 'site']},
        ),
        migrations.RemoveField(
            model_name='gcprobemeasurement',
            name='notes',
        ),
        migrations.AddField(
            model_name='species',
            name='green_crab_monitoring',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='gcprobemeasurement',
            name='cloud_cover',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='cloud cover (%)'),
        ),
        migrations.AlterField(
            model_name='gcprobemeasurement',
            name='time_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date / Time (yyyy-mm-dd hh:mm:ss)'),
        ),
        migrations.AlterField(
            model_name='gcprobemeasurement',
            name='weather_conditions',
            field=models.ManyToManyField(to='grais.WeatherConditions', verbose_name='weather conditions (ctrl+click to select multiple)'),
        ),
        migrations.AlterField(
            model_name='trap',
            name='total_green_crab_wt_kg',
            field=models.FloatField(blank=True, null=True, verbose_name='Total weight of green crabs (kg)'),
        ),
    ]
