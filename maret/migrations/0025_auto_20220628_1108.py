# Generated by Django 3.2.12 on 2022-06-28 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0012_alter_person_designation'),
        ('shared_models', '0031_subjectmatter_is_csas_request_tag'),
        ('maret', '0024_auto_20220621_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committee',
            name='branch',
            field=models.ForeignKey(blank=True, default=1, limit_choices_to=models.Q(('region__name', 'Maritimes'), models.Q(('name__contains', 'SORTING'), _negated=True), models.Q(('name__icontains', 'Fisheries Management, Resource and Aboriginal Fisheries Management'), _negated=True)), null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='committee_branch', to='shared_models.branch', verbose_name='Lead DFO Maritimes Region branch'),
        ),
        migrations.AlterField(
            model_name='committee',
            name='other_dfo_branch',
            field=models.ManyToManyField(blank=True, limit_choices_to=models.Q(('region__name', 'Maritimes'), models.Q(('name__contains', 'SORTING'), _negated=True), models.Q(('name__icontains', 'Fisheries Management, Resource and Aboriginal Fisheries Management'), _negated=True)), related_name='committee_dfo_branch', to='shared_models.Branch', verbose_name='Other participating DFO Maritimes Region branches'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='branch',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to=models.Q(('region__name', 'Maritimes'), models.Q(('name__contains', 'SORTING'), _negated=True), models.Q(('name__icontains', 'Fisheries Management, Resource and Aboriginal Fisheries Management'), _negated=True)), null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='interaction_branch', to='shared_models.branch', verbose_name='Lead DFO Maritimes branch'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='external_contact',
            field=models.ManyToManyField(blank=True, related_name='interaction_ext_contact', to='masterlist.Person', verbose_name='External contact(s)'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='other_dfo_branch',
            field=models.ManyToManyField(blank=True, limit_choices_to=models.Q(('region__name', 'Maritimes'), models.Q(('name__contains', 'SORTING'), _negated=True), models.Q(('name__icontains', 'Fisheries Management, Resource and Aboriginal Fisheries Management'), _negated=True)), related_name='interaction_dfo_branch', to='shared_models.Branch', verbose_name='Other participating DFO Maritimes Region branches'),
        ),
    ]
