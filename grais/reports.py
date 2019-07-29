import statistics
import pandas
import unicodecsv as csv
import xlsxwriter as xlsxwriter
from django.http import HttpResponse
from django.template.defaultfilters import yesno
from django.utils import timezone
from math import pi

from bokeh.io import show, export_png, export_svgs
from bokeh.models import SingleIntervalTicker, ColumnDataSource, HoverTool, LabelSet, Label, Title
from bokeh.plotting import figure, output_file, save
from bokeh import palettes
from bokeh.transform import cumsum
from django.db.models import Sum, Q
from shutil import rmtree
from django.conf import settings

from lib.functions.custom_functions import nz, listrify
from lib.functions.verbose_field_name import verbose_field_name
from . import models
import numpy as np
import os
import pandas as pd


def generate_species_sample_spreadsheet(species_list=None):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'grais', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'grais', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'normal',
         "text_wrap": True})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True})
    # Add a format. Light red fill with dark red text.
    red_format = workbook.add_format({'bg_color': '#FFC7CE',
                                      'font_color': '#9C0006'})

    # Add a format. Green fill with dark green text.
    green_format = workbook.add_format({'bg_color': '#C6EFCE',
                                        'font_color': '#006100'})

    # get a sample instance to create header
    my_sample = models.Sample.objects.first()
    my_species = models.Species.objects.first()

    # define the header
    header = [
        "Species ID",
        verbose_field_name(my_species, 'common_name'),
        verbose_field_name(my_species, 'scientific_name'),
        verbose_field_name(my_species, 'abbrev'),
        verbose_field_name(my_species, 'epibiont_type'),
        verbose_field_name(my_species, 'tsn'),
        verbose_field_name(my_species, 'aphia_id'),
        "Sample ID",
        "Observation platform",
        "Observation year",
        "Observation month",
        "Observation day",
        verbose_field_name(my_sample, 'station'),
        verbose_field_name(my_sample.station, 'province'),
        verbose_field_name(my_sample.station, 'latitude_n'),
        verbose_field_name(my_sample.station, 'longitude_w'),
        "observed at station?",
        "observed on line?",
        "observed on collector surface?",
        "% surface coverage (sample average)?",
    ]

    # worksheets #
    ##############
    new_species_list = [models.Species.objects.get(pk=int(s)) for s in species_list.split(",")]
    i = 1
    my_ws = workbook.add_worksheet(name="Samples")
    for species in new_species_list:

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
        my_ws.write_row(0, 0, header, header_format)

        # get a list of samples for each requested species FROM ALL SOURCES
        sample_list = [models.Sample.objects.get(pk=s["surface__line__sample"]) for s in
                       models.SurfaceSpecies.objects.filter(species=species).values(
                           "surface__line__sample").distinct()]
        sample_list.extend(
            [models.Sample.objects.get(pk=s["sample"]) for s in
             models.SampleSpecies.objects.filter(species=species).values(
                 "sample").distinct()]
        )
        sample_list.extend(
            [models.Sample.objects.get(pk=s["line__sample"]) for s in
             models.LineSpecies.objects.filter(species=species).values(
                 "line__sample").distinct()]
        )
        # distill the list
        sample_set = set(sample_list)

        for sample in sample_set:
            if sample.date_retrieved:
                obs_year = sample.date_retrieved.year
                obs_month = sample.date_retrieved.month
                obs_day = sample.date_retrieved.day
            else:
                obs_year = None
                obs_month = None
                obs_day = None

            if models.SampleSpecies.objects.filter(sample=sample, species=species).count() > 0:
                at_station = "yes"
            else:
                at_station = "no"

            if models.LineSpecies.objects.filter(line__sample=sample, species=species).count() > 0:
                on_line = "yes"
            else:
                on_line = "no"

            if models.SurfaceSpecies.objects.filter(surface__line__sample=sample, species=species).count() > 0:
                on_surface = "yes"
            else:
                on_surface = "no"

            # calculate the % coverage
            if on_surface:
                # for each surface, determine the percent coverage and store in list
                ## only look at plates
                coverage_list = []
                for surface in models.Surface.objects.filter(line__sample=sample).filter(surface_type="pl"):
                    try:
                        my_coverage = models.SurfaceSpecies.objects.get(surface=surface, species=species).percent_coverage
                    except:
                        my_coverage = 0
                    coverage_list.append(my_coverage)
                mean_coverage = statistics.mean(coverage_list)

            else:
                mean_coverage = "n/a"

            data_row = [
                species.id,
                species.common_name,
                species.scientific_name,
                species.abbrev,
                species.get_epibiont_type_display(),
                species.tsn,
                species.aphia_id,
                sample.id,
                'Biofouling Monitoring',
                obs_year,
                obs_month,
                obs_day,
                sample.station.station_name,
                sample.station.province.tabbrev,
                sample.station.latitude_n,
                sample.station.longitude_w,
                at_station,
                on_line,
                on_surface,
                mean_coverage,
            ]

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 100:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 100
                j += 1

            my_ws.write_row(i, 0, data_row, normal_format)
            i += 1

        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

        # set formatting for last three columns
        my_ws.conditional_format(0, header.index("observed at station?"), i,
                                 header.index("observed on collector surface?"),
                                 {
                                     'type': 'cell',
                                     'criteria': 'equal to',
                                     'value': '"yes"',
                                     'format': green_format,
                                 })
        my_ws.conditional_format(0, header.index("observed at station?"), i,
                                 header.index("observed on collector surface?"),
                                 {
                                     'type': 'cell',
                                     'criteria': 'equal to',
                                     'value': '"no"',
                                     'format': red_format,
                                 })

    workbook.close()
    return target_url


def generate_open_data_ver_1_data_dictionary():
    """
    Generates the data dictionary for open data report version 1
    """

    filename = "open_data_ver1_data_dictionary.csv"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)

    writer.writerow("")
    writer.writerow(["Abiotic variables / Variables abiotiques:".upper(), ])
    writer.writerow(["#########################################", ])
    # write the header
    header = [
        "name__nom",
        "description_en",
        "description_fr",
    ]
    writer.writerow(header)

    field_names = [
        'year',
        'site_name',
        'site_latitude',
        'site_longitude',
        'avg_air_temp_arrival',
        'avg_max_air_temp',
        'avg_water_temp_shore',
    ]

    descr_eng = [
        "sample year",
        "name of site and river",
        "site latitude (decimal degrees)",
        "site longitude (decimal degrees)",
        "average air temperature on arrival (degrees C)",
        "average max air temperature (degrees C)",
        "average water temperature taken from shore (degrees C)",
    ]
    descr_fra = [
        "année-échantillon",
        "nom du site et de la rivière",
        "latitude du site (degrés décimaux)",
        "longitude du site (degrés décimaux)",
        "température moyenne de l'air à l'arrivée (degrés C)",
        "température maximale moyenne de l'air (degrés C)",
        "température moyenne de l'eau prise du rivage (degrés C)",
    ]

    for i in range(0, len(field_names)):
        writer.writerow([
            field_names[i],
            descr_eng[i],
            descr_fra[i],
        ])

    writer.writerow("")
    writer.writerow("")
    writer.writerow("")
    writer.writerow(["Biotic variables / Variables biotiques:".upper(), ])
    writer.writerow(["#######################################", ])
    field_names = [
        "X_abundance",
        "X_avg_fork_length",
        "X_avg_weight",
    ]

    descr_eng = [
        "total abundance of species X for a given site and year",
        "mean fork length (mm) of species X for a given site and year",
        "mean weight (g) of species X for a given site and year",
    ]
    descr_fra = [
        "Abondance totale de l'espèce X pour un site et une année donnés",
        "longueur à la fourche moyenne (mm) de l'espèce X pour un site et une année donnés",
        "poids moyen (g) de l'espèce X pour un site et une année donnés",
    ]
    for i in range(0, len(field_names)):
        writer.writerow([
            field_names[i],
            descr_eng[i],
            descr_fra[i],
        ])

    writer.writerow("")
    writer.writerow("")
    writer.writerow("")
    writer.writerow(["Species / Espèces:".upper()])
    writer.writerow(["##################"])
    # write the header
    header = [
        "code",
        "common_name_en__nom_commun_en",
        "common_name_en__nom_commun_fr",
        "life_stage_en__étape_de_vie_en",
        "life_stage_fr__étape_de_vie_fr",
        "scientific_name__nom_scientifique",
        "ITIS_TSN",
    ]
    writer.writerow(header)

    for sp in models.Species.objects.all():
        life_stage_eng = sp.life_stage.name if sp.life_stage else None
        life_stage_fra = sp.life_stage.nom if sp.life_stage else None

        writer.writerow([
            sp.abbrev,
            sp.common_name_eng,
            sp.common_name_fre,
            life_stage_eng,
            life_stage_fra,
            sp.scientific_name,
            sp.tsn,
        ])

    return response


def generate_open_data_ver_1_report(year=None):
    """
    This is a view designed for FGP / open maps view.
    :param year: int
    :return: http response
    """

    # determine the filename based on whether we are looking at all years vs. a single year
    filename = "open_data_ver1_report_{}.csv".format(year) if year != "None" else "open_data_ver1_report_all_years.csv"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)

    # Botrylloïdes violaceus, Botryllus shlosseri, Caprella mutica, Ciona intestinalis, Codium fragile, Membranipora membranacea, Styela clava
    species_id_list = [48, 24, 47, 23, 55, 59, 25]
    species_qs = models.Species.objects.filter(id__in=species_id_list)

    header_row = [
        'Sampling year',
        'Station code',
        'Station name',
        'Date in',
        'Date out',
        'Weeks',
        'Station Description',
        'Collector Latitude',
        'Collector Longitude',
        'Collector ID',
        'Surface Type',
        'Surface ID',
        'Probe Type',
        'Probe Sample Date/Time',
        'Probe Depth',
        'Temperture C',
        'Sal ppt',
        'O2 percent',
        'O2 mg-l',
        'SpCond - mS',
        'Spc - mS',
        'pH',
        'Turbidity',
        'Weather Notes',
        'Samplers',
        'Other species',
    ]
    # C. intestinalis % cover,  # 23
    # B. schlosseri % cover,  # 24
    # B. schlosseri Color Morph,
    # B. violaceus % cover,  # 48
    # B. violaceus Color Morph,
    # S. clava % cover,  # 25
    # M. membranacea % cover,  # 59
    # C. mutica % cover,  # 47
    # C. fragile fragile % cover,  # 55
    for species in species_qs:
        first_name = species.scientific_name.split(" ")[0][:1].upper()
        if len(species.scientific_name.split(" ")) > 2:
            second_name = " ".join(species.scientific_name.split(" ")[1:])
        else:
            second_name = species.scientific_name.split(" ")[1]
        display_name = "{}. {}".format(first_name, second_name, )
        header_row.append("{} % cover".format(display_name))

        # if species id is 24 or 48, we want color morph notes as well
        if species.id in [24, 48]:
            header_row.append("{} Color Notes".format(display_name))

    writer.writerow(header_row)

    # lets start by getting a list of samples and years
    # samples = [models.Sample.objects.get(pk=obj["sample"]) for obj in qs.order_by("sample").values("sample").distinct()]
    # years = [obj["season"] for obj in samples.order_by("season").values("season").distinct()]

    samples = models.Sample.objects.all().order_by("date_deployed")

    # if there is a year provided, filter by only this year
    if year != "None":
        samples = samples.filter(season=year)

    # make sure to exclude the lost lines and surfaces; this is sort of redundant since if a line is line, all surfaces should also be labelled as lost.
    surfaces = models.Surface.objects.filter(
        line__sample_id__in=[obj["id"] for obj in samples.order_by("id").values("id").distinct()],
        line__is_lost=False,
        is_lost=False,
    )

    for surface in surfaces:

        # Try getting hold of the last probe sample taken
        my_probe = surface.line.sample.probe_data.order_by("time_date").last()
        if my_probe:
            probe = my_probe.probe
            time_date = my_probe.time_date.strftime("%Y-%m-%d %H:%M")
            probe_depth = my_probe.probe_depth
            temp_c = my_probe.temp_c
            sal = my_probe.sal_ppt
            o2p = my_probe.o2_percent
            o2m = my_probe.o2_mgl
            spcond = my_probe.sp_cond_ms
            spc = my_probe.spc_ms
            ph = my_probe.ph
            turb = my_probe.turbidity
            weather = my_probe.weather_notes
        else:
            probe = time_date = probe_depth = temp_c = sal = o2p = o2m = spcond = spc = ph = turb = weather = None

        # summarize all of the samplers
        samplers = listrify(["{} ({})".format(obj, obj.organization) for obj in surface.line.sample.samplers.all()])
        # summarize all of the "other" species
        other_spp = listrify([str(sp) for sp in surface.species.all() if sp.id not in species_id_list])

        data_row = [
            surface.line.sample.season,
            surface.line.sample.station_id,
            surface.line.sample.station,
            surface.line.sample.date_deployed.strftime("%Y-%m-%d"),
            surface.line.sample.date_retrieved.strftime("%Y-%m-%d") if surface.line.sample.date_retrieved else None,
            surface.line.sample.weeks_deployed,
            surface.line.sample.station.site_desc,
            surface.line.latitude_n,
            surface.line.longitude_w,
            surface.line.collector,
            surface.get_surface_type_display(),
            surface.label,
            probe, time_date, probe_depth, temp_c, sal, o2p, o2m, spcond, spc, ph, turb, weather,
            samplers,
            other_spp,
        ]

        for species in species_qs:
            try:
                data_row.append(
                    models.SurfaceSpecies.objects.get(species=species, surface=surface).percent_coverage
                )
            except models.SurfaceSpecies.DoesNotExist:

                data_row.append(
                    0
                )

            # if species id is 24 or 48, we want color morph notes as well
            if species.id in [24, 48]:
                try:
                    data_row.append(
                        models.SurfaceSpecies.objects.get(species=species, surface=surface).notes
                    )
                except models.SurfaceSpecies.DoesNotExist:
                    data_row.append(
                        None
                    )

        writer.writerow(data_row)

    return response
