# Generated by Django 3.2.4 on 2021-07-15 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0003_auto_20210715_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='sample_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='edna.sampletype', verbose_name='sample type'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='datetime',
            field=models.DateTimeField(null=True, verbose_name='collection date/time'),
        ),
    ]
