# Generated by Django 3.1.2 on 2020-12-01 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0041_auto_20201201_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusreport',
            name='project_year',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='projects2.projectyear'),
        ),
    ]
