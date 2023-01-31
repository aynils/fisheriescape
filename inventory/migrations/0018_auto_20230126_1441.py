# Generated by Django 3.2.16 on 2023-01-26 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20230126_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='metadata_freq_text',
            new_name='maintenance_text',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='metadata_update_freq',
        ),
        migrations.AlterField(
            model_name='resource',
            name='descr_eng',
            field=models.TextField(blank=True, null=True, verbose_name='Description (English)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='descr_fre',
            field=models.TextField(blank=True, null=True, verbose_name='Description (French)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='maintenance',
            field=models.IntegerField(blank=True, choices=[(2, 'Daily'), (3, 'Weekly'), (4, 'Monthly'), (5, 'Quartely'), (6, 'Annually'), (7, 'Biannual'), (8, 'Irregular'), (9, 'Continual'), (10, 'As needed'), (11, 'Not planned'), (12, 'Unknown')], help_text='What should be the expectation for how often the metadata is updated?', null=True, verbose_name='At what frequency should the metadata be updated?'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='purpose_eng',
            field=models.TextField(blank=True, null=True, verbose_name='Purpose (English)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='purpose_fre',
            field=models.TextField(blank=True, null=True, verbose_name='Purpose (French)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='title_eng',
            field=models.TextField(verbose_name='Title (English)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='title_fre',
            field=models.TextField(blank=True, null=True, verbose_name='Title (French)'),
        ),
    ]
