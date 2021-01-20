# Generated by Django 3.1.2 on 2021-01-14 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0009_auto_20201218_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='organization',
            name='org_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='number'),
        ),
        migrations.AddField(
            model_name='organization',
            name='org_site',
            field=models.URLField(blank=True, null=True, verbose_name='(spot) website'),
        ),
        migrations.AddField(
            model_name='organization',
            name='sub_org',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='sub organization'),
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='masterlist.organizationtype', verbose_name='type'),
        ),
    ]
