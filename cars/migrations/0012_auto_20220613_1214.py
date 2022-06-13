# Generated by Django 3.2.13 on 2022-06-13 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0031_subjectmatter_is_csas_request_tag'),
        ('cars', '0011_location_province'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_en', models.TextField(blank=True, null=True, verbose_name='question (en)')),
                ('question_fr', models.TextField(blank=True, null=True, verbose_name='question (fr)')),
                ('answer_en', models.TextField(blank=True, null=True, verbose_name='answer (en)')),
                ('answer_fr', models.TextField(blank=True, null=True, verbose_name='answer (fr)')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='display order')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['reference_number']},
        ),
        migrations.AlterField(
            model_name='location',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='vehicle_locations', to='shared_models.region'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.IntegerField(choices=[(1, 'Tentative'), (10, 'Approved'), (20, 'Denied'), (30, 'Field Season')], default=1, editable=False),
        ),
    ]
