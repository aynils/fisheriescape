# Generated by Django 3.1.2 on 2020-12-11 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0053_auto_20201211_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sire',
            name='indv_id',
            field=models.ForeignKey(limit_choices_to={'ufid__isnull': False}, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.individual', verbose_name='Sire UFID'),
        ),
    ]
