# Generated by Django 3.1.2 on 2021-01-15 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0012_auto_20210114_1111'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spot', '0003_auto_20210106_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgreementLineage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataQualityLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataQualityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObjectiveCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutcomeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalmonStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=255, null=True, verbose_name='number')),
                ('work_plan_sec', models.CharField(blank=True, max_length=255, null=True, verbose_name='work plan section')),
                ('task_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='task description')),
                ('key_element', models.CharField(blank=True, max_length=10, null=True, verbose_name='key element')),
                ('activity', models.CharField(blank=True, max_length=10, null=True, verbose_name='activity')),
                ('element_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='element title')),
                ('activity_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='activity title')),
                ('pst_req', models.BooleanField(default=False, verbose_name='PST requirement identified?')),
                ('duration', models.CharField(blank=True, max_length=100, null=True, verbose_name='duration')),
                ('targ_samp_num', models.CharField(blank=True, max_length=100, null=True, verbose_name='target sample number')),
                ('sil_req', models.BooleanField(default=False, verbose_name='SIL requirement')),
                ('exp_res', models.CharField(blank=True, max_length=255, null=True, verbose_name='expected results')),
                ('dfo_rep', models.CharField(blank=True, max_length=255, null=True, verbose_name='Products/Reports to provide dfo')),
                ('scientific_outcome', models.CharField(blank=True, max_length=1000, null=True, verbose_name='scientific outcome')),
                ('outcomes_deadline', models.DateField(blank=True, null=True, verbose_name='outcomes deadline')),
                ('date_last_modified', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified')),
                ('data_quality_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spot.dataqualitylevel', verbose_name='data quality level')),
                ('data_quality_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spot.dataqualitytype', verbose_name='data quality type')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='spot_person_last_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='last modified by')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='spot.location', verbose_name='location')),
                ('objective_cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spot.objectivecategory', verbose_name='Objective Category')),
                ('outcomes_cat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='spot.outcomecategory', verbose_name='outcomes category')),
                ('outcomes_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='masterlist.person', verbose_name='Outcomes Contact')),
                ('salmon_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spot.salmonstage', verbose_name='salmon stage')),
                ('samp_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='spot.sampletype', verbose_name='sample type/specific data item')),
                ('species', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spot.species', verbose_name='species')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
    ]
