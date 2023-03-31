# Generated by Django 4.1.6 on 2023-03-03 18:06

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fisheriescape", "0004_vulnerablespecies_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="VulnerableSpeciesSpot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "count",
                    models.IntegerField(blank=True, null=True, verbose_name="count"),
                ),
                (
                    "point",
                    django.contrib.gis.db.models.fields.PointField(
                        srid=4326, verbose_name="point"
                    ),
                ),
            ],
            options={
                "ordering": ["vulnerable_species", "week"],
            },
        ),
        migrations.RenameIndex(
            model_name="score",
            new_name="score_species_week",
            old_name="species_week",
        ),
        migrations.RenameIndex(
            model_name="score",
            new_name="score_week",
            old_name="week",
        ),
        migrations.RenameIndex(
            model_name="score",
            new_name="score_species",
            old_name="species",
        ),
        migrations.AddField(
            model_name="vulnerablespeciesspot",
            name="vulnerable_species",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="spots",
                to="fisheriescape.vulnerablespecies",
                verbose_name="vulnerable_species",
            ),
        ),
        migrations.AddField(
            model_name="vulnerablespeciesspot",
            name="week",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="vulnerable_species_spots",
                to="fisheriescape.week",
                verbose_name="week",
            ),
        ),
        migrations.AddIndex(
            model_name="vulnerablespeciesspot",
            index=models.Index(
                ["vulnerable_species", "week"], name="vulnerablespeciesspot_s_w"
            ),
        ),
        migrations.AddIndex(
            model_name="vulnerablespeciesspot",
            index=models.Index(["week"], name="vulnerablespeciesspot_week"),
        ),
        migrations.AddIndex(
            model_name="vulnerablespeciesspot",
            index=models.Index(["species"], name="vulnerablespeciesspot_species"),
        ),

    ]
