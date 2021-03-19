# Generated by Django 3.1.2 on 2021-03-16 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20200429_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Wish List'), ('5', 'Urgent')], default='2', max_length=1, verbose_name='priority level'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='request_type',
            field=models.IntegerField(choices=[(1, 'Software request / installation'), (2, 'System Adoption'), (3, 'Database creation'), (4, 'Data sharing / publication'), (5, 'Process development'), (6, 'Hardware'), (7, 'Data entry / digitization'), (8, 'Permissions'), (9, 'Database maintenance'), (12, 'Software issue (licensing)'), (13, 'Disk recovery'), (14, 'Hardware and software'), (15, 'Security exemption'), (16, 'App development'), (17, 'Report development'), (18, 'Other'), (19, 'App enhancement'), (20, 'Bug'), (21, 'Quality control element'), (22, 'Data transfer'), (23, 'New Shiny App')], default=20, verbose_name='type of request'),
        ),
    ]
