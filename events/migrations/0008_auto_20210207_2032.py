# Generated by Django 3.1.2 on 2021-02-08 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20210205_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='events.event'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.IntegerField(choices=[(1, 'CSAS Regional Advisory Process (RAP)'), (2, 'CSAS Science Management Meeting'), (3, 'CSAS Steering Committee Meeting'), (9, 'other')], verbose_name='type of event'),
        ),
    ]
