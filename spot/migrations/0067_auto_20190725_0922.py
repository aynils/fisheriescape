# Generated by Django 2.2.2 on 2019-07-25 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0066_auto_20190725_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='activities',
            field=models.ManyToManyField(blank=True, to='spot.Activity', verbose_name='activities'),
        ),
        migrations.AlterField(
            model_name='project',
            name='spp',
            field=models.ManyToManyField(blank=True, to='spot.Species', verbose_name='species'),
        ),
        migrations.AlterField(
            model_name='project',
            name='watersheds',
            field=models.ManyToManyField(blank=True, to='spot.Watershed', verbose_name='watersheds'),
        ),
    ]
