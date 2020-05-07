# Generated by Django 2.2.2 on 2020-04-30 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultReviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branches', models.ManyToManyField(blank=True, related_name='travel_default_reviewers', to='shared_models.Branch', verbose_name='reviewer on which DFO branch(es)')),
                ('sections', models.ManyToManyField(blank=True, related_name='travel_default_reviewers', to='shared_models.Section', verbose_name='reviewer on which DFO section(s)')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='travel_default_reviewers', to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user')),
            ],
            options={
                'ordering': ['user'],
            },
        ),
    ]
