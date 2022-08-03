import os
from datetime import datetime

import xlsxwriter as xlsxwriter
from django.conf import settings
from django.template.defaultfilters import yesno, slugify
from django.utils import timezone
from django.utils.translation import gettext as _

from lib.functions.custom_functions import nz, listrify, truncate
from lib.templatetags.verbose_names import get_verbose_label
from masterlist import models as ml_models
from shared_models.models import Region
from . import models
from .utils import get_date_range_overlap


def get_target_dir():
    dir = os.path.join(settings.BASE_DIR, 'media', 'ihub', 'temp')
    
    if not os.path.exists(dir):
        print(f"{dir} does not exist. Creating...")
        os.makedirs(dir)
    
    return dir


def generate_capacity_spreadsheet(orgs, sectors, from_date, to_date):
    # figure out the filename
    target_dir = get_target_dir()
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'ihub', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, 'num_format': '$#,##0'})

    # first, filter out the "none" placeholder
    if orgs == "None":
        orgs = None
    if sectors == "None":
        sectors = None
    if from_date == "None":
        from_date = None
    if to_date == "None":
        to_date = None

    # build an entry list:
    entry_list = models.Entry.objects.all()

    if sectors:
        # we have to refine the queryset to only the selected sectors
        sector_list = [ml_models.Sector.objects.get(pk=int(s)) for s in sectors.split(",")]
        entry_list = entry_list.filter(sectors__in=sector_list)
    if orgs:
        # we have to refine the queryset to only the selected orgs
        org_list = [ml_models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
        entry_list = entry_list.filter(organizations__in=org_list)
    else:
        # if no orgs were passed in to the report, we need to make an org list based on the orgs in the entries
        # this org_list will serve as basis for spreadsheet tabs
        org_id_list = list(set([org.id for entry in entry_list for org in entry.organizations.all()]))
        org_list = ml_models.Organization.objects.filter(id__in=org_id_list).order_by("abbrev")

    if from_date or to_date:
        id_list = []
        d0_start = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
        d0_end = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone())
        for e in entry_list:
            d1_start = e.initial_date
            d1_end = e.anticipated_end_date
            if get_date_range_overlap(d0_start, d0_end, d1_start, d1_end) > 0:
                id_list.append(e.id)
        entry_list = entry_list.filter(id__in=id_list)

    entry_list.distinct()

    # define the header
    header = [
        get_verbose_label(entry_list.first(), 'fiscal_year'),
        get_verbose_label(entry_list.first(), 'title'),
        get_verbose_label(entry_list.first(), 'organizations'),
        get_verbose_label(entry_list.first(), 'status'),
        get_verbose_label(entry_list.first(), 'sectors'),
        get_verbose_label(entry_list.first(), 'entry_type'),
        get_verbose_label(entry_list.first(), 'initial_date'),
        get_verbose_label(entry_list.first(), 'anticipated_end_date'),
        get_verbose_label(entry_list.first(), 'regions'),
        get_verbose_label(entry_list.first(), 'funding_program'),
        get_verbose_label(entry_list.first(), 'funding_needed'),
        get_verbose_label(entry_list.first(), 'funding_purpose'),
        get_verbose_label(entry_list.first(), 'amount_requested'),
        get_verbose_label(entry_list.first(), 'amount_approved'),
        get_verbose_label(entry_list.first(), 'amount_transferred'),
        get_verbose_label(entry_list.first(), 'amount_lapsed'),
        _("Amount outstanding"),
    ]

    # worksheets #
    ##############

    for org in org_list:
        my_ws = workbook.add_worksheet(name=org.abbrev)

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
        my_ws.write(0, 0, str(org), title_format)
        my_ws.write_row(2, 0, header, header_format)

        tot_requested = 0
        tot_approved = 0
        tot_transferred = 0
        tot_lapsed = 0
        tot_outstanding = 0
        i = 3
        for e in entry_list.filter(organizations=org):

            if e.organizations.count() > 0:
                orgs = str([str(obj) for obj in e.organizations.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"',
                                                                                                                                   "")
            else:
                orgs = None

            if e.sectors.count() > 0:
                sectors = str([str(obj) for obj in e.sectors.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            else:
                sectors = None

            if e.regions.count() > 0:
                regions = str([str(obj) for obj in e.regions.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            else:
                regions = None

            data_row = [
                e.fiscal_year,
                e.title,
                orgs,
                str(e.status),
                sectors,
                str(e.entry_type),
                e.initial_date.strftime("%Y-%m-%d") if e.initial_date else "n/a",
                e.anticipated_end_date.strftime("%Y-%m-%d") if e.anticipated_end_date else "",
                regions,
                nz(str(e.funding_program), ""),
                nz(str(e.funding_needed), ""),
                nz(str(e.funding_purpose), ""),
                nz(e.amount_requested, 0),
                nz(e.amount_approved, 0),
                nz(e.amount_transferred, 0),
                nz(e.amount_lapsed, 0),
                nz(e.amount_outstanding, 0),
            ]

            tot_requested += nz(e.amount_requested, 0)
            tot_approved += nz(e.amount_approved, 0)
            tot_transferred += nz(e.amount_transferred, 0)
            tot_lapsed += nz(e.amount_lapsed, 0)
            tot_outstanding += nz(e.amount_outstanding, 0)

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

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

        # sum all the currency columns
        total_row = [
            _("GRAND TOTAL:"),
            tot_requested,
            tot_approved,
            tot_transferred,
            tot_lapsed,
            tot_outstanding,
        ]
        try:
            my_ws.write_row(i + 2, header.index(_("Funding requested")) - 1, total_row, total_format)

            # set formatting for status
            for status in models.Status.objects.all():
                my_ws.conditional_format(0, header.index(_("status").title()), i, header.index(_("status").title()),
                                         {
                                             'type': 'cell',
                                             'criteria': 'equal to',
                                             'value': '"{}"'.format(status.name),
                                             'format': workbook.add_format({'bg_color': status.color, }),
                                         })

            # set formatting for entry type
            for entry_type in models.EntryType.objects.all():
                my_ws.conditional_format(0, header.index(_("Entry Type").title()), i, header.index(_("Entry Type").title()),
                                         {
                                             'type': 'cell',
                                             'criteria': 'equal to',
                                             'value': '"{}"'.format(entry_type.name),
                                             'format': workbook.add_format({'bg_color': entry_type.color, }),
                                         })
        except:
            print("problem with summary row")

    workbook.close()
    return target_url


def generate_summary_spreadsheet(orgs, sectors, from_date, to_date, entry_note_types, entry_note_statuses):
    # figure out the filename
    target_dir = get_target_dir()
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'ihub', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, 'num_format': '$#,##0'})

    # first, filter out the "none" placeholder
    if sectors == "None":
        sectors = None
    if orgs == "None":
        orgs = None
    if from_date == "None":
        from_date = None
    if to_date == "None":
        to_date = None
    if entry_note_types == "None":
        entry_note_types = None
    else:
        entry_note_types = [int(i) for i in entry_note_types.split(",")] if entry_note_types else None

    if entry_note_statuses == "None":
        entry_note_statuses = None
    else:
        entry_note_statuses = [int(i) for i in entry_note_statuses.split(",")] if entry_note_statuses else None
    # build an entry list:
    entry_list = models.Entry.objects.all()

    if sectors:
        # we have to refine the queryset to only the selected sectors
        sector_list = [ml_models.Sector.objects.get(pk=int(s)) for s in sectors.split(",")]
        entry_list = entry_list.filter(sectors__in=sector_list)
    if orgs:
        # we have to refine the queryset to only the selected orgs
        org_list = [ml_models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
        entry_list = entry_list.filter(organizations__in=org_list)
    else:
        # if no orgs were passed in to the report, we need to make an org list based on the orgs in the entries
        # this org_list will serve as basis for spreadsheet tabs
        org_id_list = list(set([org.id for entry in entry_list for org in entry.organizations.all()]))
        org_list = ml_models.Organization.objects.filter(id__in=org_id_list).order_by("abbrev")

    if from_date or to_date:
        id_list = []
        d0_start = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone()) if from_date else None
        d0_end = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone()) if to_date else None
        for e in entry_list:
            d1_start = e.initial_date
            d1_end = e.anticipated_end_date
            if get_date_range_overlap(d0_start, d0_end, d1_start, d1_end) > 0:
                id_list.append(e.id)
        entry_list = entry_list.filter(id__in=id_list)

    entry_list.distinct()

    # define the header
    header = [
        get_verbose_label(entry_list.first(), 'fiscal_year'),
        get_verbose_label(entry_list.first(), 'title'),
        get_verbose_label(entry_list.first(), 'organizations'),
        get_verbose_label(entry_list.first(), 'status'),
        get_verbose_label(entry_list.first(), 'sectors'),
        get_verbose_label(entry_list.first(), 'entry_type'),
        get_verbose_label(entry_list.first(), 'initial_date'),
        get_verbose_label(entry_list.first(), 'anticipated_end_date'),
        get_verbose_label(entry_list.first(), 'regions'),
        _("DFO Contacts"),
        _("Notes"),
        get_verbose_label(entry_list.first(), 'funding_program'),
        get_verbose_label(entry_list.first(), 'funding_needed'),
        get_verbose_label(entry_list.first(), 'funding_purpose'),
        get_verbose_label(entry_list.first(), 'amount_requested'),
        get_verbose_label(entry_list.first(), 'amount_approved'),
        get_verbose_label(entry_list.first(), 'amount_transferred'),
        get_verbose_label(entry_list.first(), 'amount_lapsed'),
        _("Amount outstanding"),
    ]

    # worksheets #
    ##############

    # each org should be represented on a separate worksheet
    # therefore determine an appropriate org list
    org_counter = 0
    for org in org_list:
        org_abbrev = slugify(org.abbrev) if org.abbrev else f"missing_abbrev_{org_counter}"
        org_counter += 1
        my_ws = workbook.add_worksheet(name=org_abbrev)

        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
        my_ws.write(0, 0, str(org), title_format)
        my_ws.write_row(2, 0, header, header_format)

        tot_requested = 0
        tot_approved = 0
        tot_transferred = 0
        tot_lapsed = 0
        tot_outstanding = 0
        i = 3
        for e in entry_list.filter(organizations=org):

            if e.organizations.count() > 0:
                orgs = str([str(obj) for obj in e.organizations.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"',
                                                                                                                                   "").replace(
                    ', ', "\n")
            else:
                orgs = None

            if e.people.count() > 0:
                people = str(["{} - {} ({})".format(obj.get_role_display(), obj, obj.organization) for obj in e.people.all()]).replace(
                    "[", "").replace("]", "").replace("'", "").replace('"', "").replace(', ', "\n")
            else:
                people = None
            note_qry = e.notes.all()
            if note_qry.count() > 0:
                notes = ""
                count = 0
                max_count = note_qry.count()
                for obj in note_qry:
                    if not entry_note_types or (obj.type in entry_note_types):
                        if not entry_note_statuses or (obj.status_id in entry_note_statuses):
                            notes += "{} - {} [STATUS: {}] (Created by {} {} on {})\n".format(
                                obj.get_type_display().upper(),
                                obj.note,
                                obj.status,
                                obj.author.first_name if obj.author else "",
                                obj.author.last_name if obj.author else "",
                                obj.creation_date.strftime("%Y-%m-%d"),
                            )
                            if not count == max_count:
                                notes += "\n"
            else:
                notes = None

            if e.sectors.count() > 0:
                sectors = str([str(obj) for obj in e.sectors.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"',
                                                                                                                                "").replace(
                    ', ', "\n")
            else:
                sectors = None

            if e.regions.count() > 0:
                regions = str([str(obj) for obj in e.regions.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            else:
                regions = None

            data_row = [
                e.fiscal_year,
                e.title,
                orgs,
                str(e.status),
                sectors,
                str(e.entry_type),
                e.initial_date.strftime("%Y-%m-%d") if e.initial_date else "n/a",
                e.anticipated_end_date.strftime("%Y-%m-%d") if e.anticipated_end_date else "",
                regions,
                people,
                notes,
                nz(str(e.funding_program), ""),
                yesno(e.funding_needed),
                nz(str(e.funding_purpose), ""),
                nz(e.amount_requested, 0),
                nz(e.amount_approved, 0),
                nz(e.amount_transferred, 0),
                nz(e.amount_lapsed, 0),
                nz(e.amount_outstanding, 0),
            ]

            tot_requested += nz(e.amount_requested, 0)
            tot_approved += nz(e.amount_approved, 0)
            tot_transferred += nz(e.amount_transferred, 0)
            tot_lapsed += nz(e.amount_lapsed, 0)
            tot_outstanding += nz(e.amount_outstanding, 0)

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 75:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 75
                j += 1

            my_ws.write_row(i, 0, data_row, normal_format)
            i += 1

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

        # sum all the currency columns
        total_row = [
            _("GRAND TOTAL:"),
            tot_requested,
            tot_approved,
            tot_transferred,
            tot_lapsed,
            tot_outstanding,
        ]
        try:
            my_ws.write_row(i + 2, header.index(_("Funding requested")) - 1, total_row, total_format)

            # set formatting for status
            for status in models.Status.objects.all():
                my_ws.conditional_format(0, header.index(_("status").title()), i, header.index(_("status").title()),
                                         {
                                             'type': 'cell',
                                             'criteria': 'equal to',
                                             'value': '"{}"'.format(status.name),
                                             'format': workbook.add_format({'bg_color': status.color, }),
                                         })

            # set formatting for entry type
            for entry_type in models.EntryType.objects.all():
                my_ws.conditional_format(0, header.index(_("Entry Type").title()), i, header.index(_("Entry Type").title()),
                                         {
                                             'type': 'cell',
                                             'criteria': 'equal to',
                                             'value': '"{}"'.format(entry_type.name),
                                             'format': workbook.add_format({'bg_color': entry_type.color, }),
                                         })
        except:
            print("problem with summary row")
        i += 1

    workbook.close()
    return target_url


def generate_consultation_log_spreadsheet(orgs, sectors, statuses, entry_types, report_title, from_date, to_date, entry_note_types,
                                          entry_note_statuses):
    # figure out the filename
    target_dir = get_target_dir()
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'ihub', 'temp', target_file)

    # first, filter out the "none" placeholder
    if sectors == "None":
        sectors = None
    if orgs == "None":
        orgs = None
    if statuses == "None":
        statuses = None
    if entry_types == "None":
        entry_types = None
    if from_date == "None":
        from_date = None
    if to_date == "None":
        to_date = None
    if entry_note_types == "None":
        entry_note_types = None
    else:
        entry_note_types = [int(i) for i in entry_note_types.split(",")] if entry_note_types else None
    if entry_note_statuses == "None":
        entry_note_statuses = None
    else:
        entry_note_statuses = [int(i) for i in entry_note_statuses.split(",")] if entry_note_statuses else None

    # get an entry list for the fiscal year (if any)
    entry_list = models.Entry.objects.all().order_by("status", "-initial_date")

    if orgs:
        # we have to refine the queryset to only the selected orgs
        org_list = [ml_models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
        entry_list = entry_list.filter(organizations__in=org_list)

    if sectors:
        # we have to refine the queryset to only the selected sectors
        sector_list = [ml_models.Sector.objects.get(pk=int(s)) for s in sectors.split(",")]
        entry_list = entry_list.filter(sectors__in=sector_list)

    if statuses:
        # we have to refine the queryset to only the selected statuses
        status_list = [models.Status.objects.get(pk=int(o)) for o in statuses.split(",")]
        entry_list = entry_list.filter(status__in=status_list)

    if entry_types:
        # we have to refine the queryset to only the selected orgs
        entry_type_list = [models.EntryType.objects.get(pk=int(o)) for o in entry_types.split(",")]
        entry_list = entry_list.filter(entry_type__in=entry_type_list)

    if from_date or to_date:
        id_list = []
        d0_start = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone()) if from_date else None
        d0_end = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone()) if to_date else None
        for e in entry_list:
            d1_start = e.initial_date
            d1_end = e.anticipated_end_date
            if get_date_range_overlap(d0_start, d0_end, d1_start, d1_end) > 0:
                id_list.append(e.id)
        entry_list = entry_list.filter(id__in=id_list)

    entry_list.distinct()

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#a6cbf5', "align": 'normal', "text_wrap": True,
         "valign": 'top', })
    normal_format = workbook.add_format({
        "align": 'left', "text_wrap": True, 'num_format': 'mm/dd/yyyy', "valign": 'top',
    })

    # define the header
    header = [
        "Project title",
        "Proponent",
        "Location",
        "Type if interaction",
        "Indigenous Group(s)",
        "Date offer to Consult",
        "Departments Involved\n(Prov & Fed)",
        "Project Status/ Correspondence / Notes",
        "Follow-up Actions required",
    ]

    my_ws = workbook.add_worksheet(name="report")

    # create the col_max column to store the length of each header
    # should be a maximum column width to 100
    col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
    my_ws.write(0, 0, report_title, title_format)
    my_ws.write_row(2, 0, header, header_format)
    i = 3
    for e in entry_list.all():
        sectors = f"\n\nDFO SECTORS: {e.sectors_str,}"
        people = nz(listrify([p for p in e.people.all()], "\n\n"), "") + nz(sectors, "")

        other_notes = "Overall status: {}".format(e.status)
        if e.other_notes.count() > 0:
            for n in e.other_notes.all():
                if not entry_note_types or (n.type in entry_note_types):
                    if not entry_note_statuses or (n.status_id in entry_note_statuses):
                        other_notes += "\n\n*************************\n" + str(n)

        followups = ""
        for n in e.followups.all():
            if len(followups) == 0:
                followups = str(n)
            else:
                followups += "\n\n*************************\n" + str(n)

        data_row = [
            e.title,
            e.proponent,
            nz(e.location, "----"),
            str(e.entry_type),
            e.orgs_str,
            e.initial_date.strftime("%m/%d/%Y") if e.initial_date else "n/a",
            people,
            other_notes.replace("\\r\\n", "\r\n"),
            followups.replace("\\r\\n", "\r\n") if followups else "",
        ]

        # adjust the width of the columns based on the max string length in each col
        ## replace col_max[j] if str length j is bigger than stored value

        j = 0
        for d in data_row:
            # if new value > stored value... replace stored value
            if len(str(d)) > col_max[j]:
                if len(str(d)) < 75:
                    col_max[j] = len(str(d))
                else:
                    col_max[j] = 75
            j += 1

        my_ws.write_row(i, 0, data_row, normal_format)
        i += 1

    # set column widths
    for j in range(0, len(col_max)):
        my_ws.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url


def consultation_instructions_export_spreadsheet(orgs=None):
    # figure out the filename
    target_dir = get_target_dir()
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'ihub', 'temp', target_file)

    # first, filter out the "none" placeholder
    orgs = None if orgs == "None" else orgs

    # if there are some organizations that are specified,
    if orgs:
        # we have to refine the queryset to only the selected orgs
        object_list = ml_models.ConsultationInstruction.objects.filter(organization_id__in=orgs.split(","))
    else:
        # else return all orgs
        object_list = ml_models.ConsultationInstruction.objects.all()

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#a6cbf5', "align": 'normal', "text_wrap": True,
         "valign": 'top', })
    normal_format = workbook.add_format({
        "align": 'left', "text_wrap": True, 'num_format': 'mm/dd/yyyy', "valign": 'top',
    })

    # define the header
    header = [
        "Community",
        "Address Letter To",
        "cc: on Bottom of Letter",
        "Mailing Address",
        "Chief/Primary Point of Contact Name",
        "Chief/Primary Point of Contact Email",
        "Chief/Primary Point of Contact Phone",
        "Paper Copy",
        "To",
        "Cc",
        "Cc Commercial",
    ]

    my_ws = workbook.add_worksheet(name="mail_merge")

    # create the col_max column to store the length of each header
    # should be a maximum column width to 100
    col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
    my_ws.write_row(0, 0, header, header_format)
    i = 1
    for obj in object_list.all():

        data_row = [
            str(obj.organization),
            obj.letter_to,
            obj.letter_cc,
            obj.organization.full_address,
            obj.organization.chief.person.full_name if obj.organization.chief else "",
            obj.organization.chief.person.email_1 if obj.organization.chief else "",
            obj.organization.chief.person.phone_1 if obj.organization.chief else "",
            obj.paper_copy,
            listrify([consultee.member.person.email_1 for consultee in obj.to_email_recipients.all()], "; "),
            listrify([consultee.member.person.email_1 for consultee in obj.cc_email_recipients.all()], "; "),
            listrify([consultee.member.person.email_1 for consultee in obj.cc_commercial_email_recipients.all()], "; "),
        ]

        # adjust the width of the columns based on the max string length in each col
        ## replace col_max[j] if str length j is bigger than stored value

        j = 0
        for d in data_row:
            # if new value > stored value... replace stored value
            if len(str(d)) > col_max[j]:
                if len(str(d)) < 75:
                    col_max[j] = len(str(d))
                else:
                    col_max[j] = 75
            j += 1

        my_ws.write_row(i, 0, data_row, normal_format)
        i += 1
    # set column widths
    for j in range(0, len(col_max)):
        my_ws.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url


def generate_consultation_report(orgs, sectors, statuses, from_date, to_date, entry_note_types,
                                 entry_note_statuses, org_regions, entry_regions):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'temp', target_file)

    # first, filter out the "none" placeholder
    if sectors == "None":
        sectors = None
    if orgs == "None":
        orgs = None
    if statuses == "None":
        statuses = None
    if from_date == "None":
        from_date = None
    if to_date == "None":
        to_date = None
    if org_regions == "None":
        org_regions = None
    if entry_regions == "None":
        entry_regions = None

    if entry_note_types == "None":
        entry_note_types = None
    else:
        entry_note_types = [int(i) for i in entry_note_types.split(",")] if entry_note_types else None

    if entry_note_statuses == "None":
        entry_note_statuses = None
    else:
        entry_note_statuses = [int(i) for i in entry_note_statuses.split(",")] if entry_note_statuses else None

    # get an entry list for the fiscal year (if any)
    entry_list = models.Entry.objects.filter(entry_type__name__icontains="consultation").order_by("status", "-initial_date")

    if org_regions:
        # we have to refine the queryset to only the selected orgs
        region_list = [Region.objects.get(pk=int(o)) for o in org_regions.split(",")]
        entry_list = entry_list.filter(organizations__regions__in=region_list)

    if entry_regions:
        # we have to refine the queryset to only the selected orgs
        region_list = [Region.objects.get(pk=int(o)) for o in entry_regions.split(",")]
        entry_list = entry_list.filter(regions__in=region_list)

    if orgs:
        # we have to refine the queryset to only the selected orgs
        org_list = [ml_models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
        entry_list = entry_list.filter(organizations__in=org_list)

    if sectors:
        # we have to refine the queryset to only the selected sectors
        sector_list = [ml_models.Sector.objects.get(pk=int(s)) for s in sectors.split(",")]
        entry_list = entry_list.filter(sectors__in=sector_list)

    if statuses:
        # we have to refine the queryset to only the selected statuses
        status_list = [models.Status.objects.get(pk=int(o)) for o in statuses.split(",")]
        entry_list = entry_list.filter(status__in=status_list)

    if from_date or to_date:
        id_list = []
        d0_start = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone()) if from_date else None
        d0_end = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.get_current_timezone()) if to_date else None
        for e in entry_list:
            d1_start = e.initial_date
            d1_end = e.anticipated_end_date
            if get_date_range_overlap(d0_start, d0_end, d1_start, d1_end) > 0:
                id_list.append(e.id)
        entry_list = entry_list.filter(id__in=id_list)

    entry_list.distinct()

    workbook = xlsxwriter.Workbook(target_file_path)
    # create formatting
    title_format = workbook.add_format({'bold': True, "align": 'normal', 'font_size': 24, })
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#a6cbf5', "align": 'normal', "text_wrap": True,
         "valign": 'top', })
    normal_format = workbook.add_format({
        "align": 'left', "text_wrap": True, 'num_format': 'mm/dd/yyyy', "valign": 'top',
    })
    highlighted_format = workbook.add_format({
        "align": 'left', "text_wrap": True, 'num_format': 'mm/dd/yyyy', "valign": 'top', "bg_color": "yellow"
    })

    # we want a sheet for every sector
    sector_ids = []
    for e in entry_list:
        for s in e.sectors.all():
            sector_ids.append(s.id)

    sectors = ml_models.Sector.objects.filter(id__in=sector_ids)
    # there is a problem: some of the sectors have duplicate names, especially when truncated..
    for s in sectors:
        sector_name = truncate(s.name, 30, False)
        if sectors.filter(name__icontains=sector_name).count() > 1:
            sector_name = truncate(s.name, 25, False) + f" ({s.id})"
        my_ws = workbook.add_worksheet(name=sector_name)
        entries = s.entries.filter(id__in=[e.id for e in entry_list])

        # define the header
        header = [
            "Title",
            "Organizations",
            "Status",
            "Persons/lead",
            "DFO programs involved",
            "letter sent",
            "Response Requested by",
            "Proponent",
            "FAA Required? (Yes/No)",
            "FAA Issued? (Yes/No)",
            "Comments",
        ]


        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
        my_ws.write_row(0, 0, header, header_format)
        i = 1
        for e in entries.all():
            people = nz(listrify([p for p in e.people.all()], "\n\n"), "")
            notes = ""
            if e.notes.exists():
                for n in e.notes.all():
                    if not entry_note_types or (n.type in entry_note_types):
                        if not entry_note_statuses or (n.status_id in entry_note_statuses):
                            if len(notes):
                                notes += "\n\n*************************\n" + str(n)
                            else:
                                notes = str(n)

            data_row = [
                e.title,
                e.orgs_str,
                str(e.status),
                people,
                e.sectors_str,
                e.initial_date.strftime("%m/%d/%Y") if e.initial_date else " ---",
                e.response_requested_by.strftime("%m/%d/%Y") if e.response_requested_by else " ---",
                e.proponent,
                yesno(e.is_faa_required, "yes,no,no"),
                yesno(e.is_faa_issued, "yes,no,no"),
                notes.replace("\\r\\n", "\r\n"),
            ]

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            j = 0
            for d in data_row:
                # if new value > stored value... replace stored value
                if len(str(d)) > col_max[j]:
                    if len(str(d)) < 75:
                        col_max[j] = len(str(d))
                    else:
                        col_max[j] = 75
                j += 1
            format = normal_format
            if e.sectors.count() > 1:
                format = highlighted_format
            my_ws.write_row(i, 0, data_row, format)
            i += 1

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url
