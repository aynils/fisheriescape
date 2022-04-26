# Generated by Django 3.2.10 on 2022-04-25 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edna', '0038_auto_20220425_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionbatch',
            name='default_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='edna.collection', verbose_name='default project'),
        ),
        migrations.AddField(
            model_name='filtrationbatch',
            name='default_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='edna.collection', verbose_name='default project'),
        ),
        migrations.AddField(
            model_name='pcrbatch',
            name='default_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='edna.collection', verbose_name='default project'),
        ),
    ]
