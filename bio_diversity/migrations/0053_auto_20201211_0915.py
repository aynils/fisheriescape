# Generated by Django 3.1.2 on 2020-12-11 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0052_auto_20201211_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='pit_tag',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='PIT tag ID'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='ufid',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ABL Fish UFID'),
        ),
    ]
