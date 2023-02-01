# Generated by Django 3.2.16 on 2023-02-01 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0007_auto_20230125_0932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dnaextract',
            options={'ordering': ['extraction_batch', 'order', 'filter__tube_id', 'id']},
        ),
        migrations.RemoveField(
            model_name='pcr',
            name='master_mix',
        ),
        migrations.AddField(
            model_name='assay',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='Is this assay in use?'),
        ),
        migrations.AddField(
            model_name='assay',
            name='master_mix',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pcrs', to='edna.mastermix', verbose_name='master mix'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='tube_id',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True, verbose_name='tube ID'),
        ),
        migrations.AlterField(
            model_name='pcrassay',
            name='result',
            field=models.IntegerField(choices=[(8, 'in progress'), (1, 'positive'), (0, 'negative'), (90, 'no assay :('), (91, 'LOD missing :('), (92, 'Inconclusive'), (93, 'Suspected')], default=8, editable=False, verbose_name='result'),
        ),
    ]
