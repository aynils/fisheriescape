# Generated by Django 3.1.2 on 2020-12-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0032_auto_20201207_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumentdet',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='instrumentdet',
            name='start_date',
            field=models.DateField(verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='location',
            name='loc_date',
            field=models.DateTimeField(verbose_name='Date event took place'),
        ),
        migrations.AlterField(
            model_name='program',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='program',
            name='start_date',
            field=models.DateField(verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='start_date',
            field=models.DateField(verbose_name='Start Date'),
        ),
    ]
