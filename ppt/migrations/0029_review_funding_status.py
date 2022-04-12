# Generated by Django 3.2.10 on 2022-04-12 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt', '0028_alter_dma_cloud_costs'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='funding_status',
            field=models.IntegerField(blank=True, choices=[(1, 'fully funded'), (2, 'partially funded'), (3, 'unfunded')], null=True, verbose_name='funding status'),
        ),
    ]
