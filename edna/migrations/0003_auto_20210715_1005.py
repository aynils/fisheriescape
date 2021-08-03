# Generated by Django 3.2.4 on 2021-07-15 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0002_sampletype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dnaextract',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='filter',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='sample',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='sample',
            name='site_description',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='site_identifier',
        ),
        migrations.AddField(
            model_name='sample',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='location'),
        ),
        migrations.AddField(
            model_name='sample',
            name='site',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='site'),
        ),
        migrations.AddField(
            model_name='sample',
            name='station',
            field=models.TextField(blank=True, null=True, verbose_name='station'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='samplers',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='collector name'),
        ),
    ]
