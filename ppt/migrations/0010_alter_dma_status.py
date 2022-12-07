# Generated by Django 3.2.14 on 2022-12-07 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt', '0009_auto_20221116_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dma',
            name='status',
            field=models.IntegerField(choices=[(0, 'Unevaluated'), (1, 'On-track'), (2, 'Complete'), (3, 'Encountering issues'), (4, 'Aborted / cancelled'), (5, 'Pending new evaluation')], default=3, editable=False),
        ),
    ]
