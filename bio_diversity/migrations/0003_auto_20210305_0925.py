# Generated by Django 3.1.2 on 2021-03-05 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bio_diversity', '0002_auto_20210301_0930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anidetsubjcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='cup',
            options={'ordering': ['facic_id', 'name']},
        ),
        migrations.AlterModelOptions(
            name='eventcode',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='heathunit',
            options={'ordering': ['facic_id', 'name']},
        ),
        migrations.AlterModelOptions(
            name='tank',
            options={'ordering': ['facic_id', 'name']},
        ),
        migrations.AlterModelOptions(
            name='tray',
            options={'ordering': ['facic_id', 'name']},
        ),
        migrations.AlterModelOptions(
            name='trough',
            options={'ordering': ['facic_id', 'name']},
        ),
        migrations.AddField(
            model_name='pairing',
            name='pair_prio_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pair_priorities', to='bio_diversity.prioritycode', verbose_name='Priority of Pair'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pairing',
            name='prio_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='female_priorities', to='bio_diversity.prioritycode', verbose_name='Priority of Female'),
        ),
    ]
