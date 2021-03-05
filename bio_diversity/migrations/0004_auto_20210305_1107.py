# Generated by Django 3.1.2 on 2021-03-05 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0003_auto_20210305_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='count',
            name='contx_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counts', to='bio_diversity.containerxref', verbose_name='Container Cross Reference'),
        ),
        migrations.AlterField(
            model_name='count',
            name='loc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counts', to='bio_diversity.location', verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='sire',
            name='indv_id',
            field=models.ForeignKey(limit_choices_to={'indv_valid': True, 'pit_tag__isnull': False}, on_delete=django.db.models.deletion.CASCADE, related_name='sires', to='bio_diversity.individual', verbose_name='Sire'),
        ),
    ]
