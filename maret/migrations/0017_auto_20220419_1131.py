# Generated by Django 3.2.12 on 2022-04-19 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maret', '0016_alter_committee_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='committee',
            name='area_office',
        ),
        migrations.AddField(
            model_name='committee',
            name='area_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='committee_area_office', to='maret.areaoffice', verbose_name='Lead Area Office'),
        ),
        migrations.AlterField(
            model_name='committee',
            name='meeting_frequency',
            field=models.IntegerField(choices=[(0, 'Monthly'), (1, 'Once a year'), (3, 'Twice a year'), (5, 'Three times a year'), (6, 'Four times a year'), (7, 'As needed'), (8, 'Every other year'), (9, 'Other')], default=1, verbose_name='Meeting frequency'),
        ),
    ]
