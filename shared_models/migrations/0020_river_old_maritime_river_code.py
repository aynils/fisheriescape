# Generated by Django 2.2.2 on 2019-07-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0019_auto_20190712_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='river',
            name='old_maritime_river_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
