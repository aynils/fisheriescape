# Generated by Django 2.1.4 on 2019-01-03 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0010_digestionlevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prey',
            name='digestion_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='diets.DigestionLevel'),
        ),
    ]
