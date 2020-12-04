# Generated by Django 3.1.2 on 2020-12-04 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0024_auto_20201204_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseSiteCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description (en)')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='Description (fr)')),
                ('created_by', models.CharField(max_length=32, verbose_name='Created By')),
                ('created_date', models.DateField(verbose_name='Created Date')),
                ('min_lat', models.DecimalField(blank=True, decimal_places=5, max_digits=7, null=True, verbose_name='Min Lattitude')),
                ('min_lon', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, verbose_name='Min Longitude')),
                ('max_lat', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, verbose_name='Min Longitude')),
                ('rive_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.rivercode', verbose_name='River')),
                ('subr_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.subrivercode', verbose_name='SubRiver Code')),
                ('trib_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.tributary', verbose_name='Tributary')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=32, verbose_name='Created By')),
                ('created_date', models.DateField(verbose_name='Created Date')),
                ('loc_lat', models.DecimalField(blank=True, decimal_places=5, max_digits=7, null=True, verbose_name='Lattitude')),
                ('loc_lon', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, verbose_name='Longitude')),
                ('loc_date', models.DateField(verbose_name='Date event took place')),
                ('loc_time', models.TimeField(blank=True, null=True, verbose_name='Time event took place')),
                ('comments', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Comments')),
                ('evnt_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.event', verbose_name='Event')),
                ('locc_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.loccode', verbose_name='Location Code')),
                ('relc_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.releasesitecode', verbose_name='SubRiver Code')),
                ('rive_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.rivercode', verbose_name='River')),
                ('subr_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.subrivercode', verbose_name='SubRiver Code')),
                ('trib_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bio_diversity.tributary', verbose_name='Tributary')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
