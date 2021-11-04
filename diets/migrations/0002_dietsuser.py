# Generated by Django 3.2.5 on 2021-11-04 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='app administrator?')),
                ('is_crud_user', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='CRUD permissions?')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='diets_user', to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user')),
            ],
            options={
                'ordering': ['-is_admin', 'user__first_name'],
            },
        ),
    ]
