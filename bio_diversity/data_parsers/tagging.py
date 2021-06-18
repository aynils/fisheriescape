from django.core.exceptions import ValidationError
from django.db import IntegrityError
import pandas as pd
from django.db.models.functions import Length

from bio_diversity import models
from bio_diversity import utils
from bio_diversity.utils import DataParser


class TaggingParser(DataParser):
    to_tank_key = "To Tank"
    from_tank_key = "From Tank"
    group_key = "Group"
    stok_key = "Stock"
    ufid_key = "Universal Fish ID"
    pit_key = "PIT Tag #"
    comment_key = "Comments"
    len_key = "Length (cm)"
    len_key_mm = "Length (mm)"
    weight_key = "Weight (g)"
    weight_key_kg = "Weight (kg)"
    vial_key = "Vial"
    crew_key = "Tagger"
    precocity_key = "Precocity (Y/N)"

    header = 0
    converters = {to_tank_key: str, from_tank_key: str, 'Year': str, 'Month': str, 'Day': str}
    start_grp_dict = {}
    end_grp_dict = {}

    tagger_code = None
    salmon_id = None
    stok_id = None
    coll_id = None
    grp_id = None
    anix_indv = None

    vial_anidc_id = None
    len_anidc_id = None
    weight_anidc_id = None
    ani_health_anidc_id = None

    def data_preper(self):
        if len(self.data[self.group_key].unique()) > 1 or len(self.data[self.stok_key].unique()) > 1:
            self.log_data += "\n WARNING: Form only designed for use with single group. Check \"Group\" column and" \
                             " split sheet if needed. \n"

        self.tagger_code = models.RoleCode.objects.filter(name__iexact="Tagger").get()
        self.salmon_id = models.SpeciesCode.objects.filter(name__iexact="Salmon").get()
        self.vial_anidc_id = models.AnimalDetCode.objects.filter(name="Vial").get()
        self.len_anidc_id = models.AnimalDetCode.objects.filter(name="Length").get()
        self.weight_anidc_id = models.AnimalDetCode.objects.filter(name="Weight").get()
        self.ani_health_anidc_id = models.AnimalDetCode.objects.filter(name="Animal Health").get()

        year, coll = utils.year_coll_splitter(self.data[self.group_key][0])
        grp_qs = models.Group.objects.filter(stok_id__name=self.data_dict[0][self.stok_key],
                                             coll_id__name__icontains=coll,
                                             grp_year=year)
        if len(grp_qs) == 1:
            self.grp_id = grp_qs.get().pk
        elif len(grp_qs) > 1:
            for grp in grp_qs:
                tank_list = grp.current_tank()
                if str(self.data[self.from_tank_key][0]) in [tank.name for tank in tank_list]:
                    self.grp_id = grp.pk

        if self.grp_id:
            utils.enter_anix(self.cleaned_data, grp_pk=self.grp_id, return_sucess=False)
        else:
            raise Exception("Parent group not found in database.  No group with tag {}-{}-{} presnt in tank"
                            " {}.".format(self.data[self.stok_key], year, coll, self.data[self.from_tank_key][0]))
        self.stok_id = models.StockCode.objects.filter(name=self.data[self.stok_key][0]).get()
        self.coll_id = models.Collection.objects.filter(name__icontains=coll).get()

    def row_parser(self, row):
        cleaned_data = self.cleaned_data
        year, coll = utils.year_coll_splitter(row[self.group_key])
        row_datetime = utils.get_row_date(row)
        row_date = row_datetime.date()
        indv_ufid = utils.nan_to_none(row.get(self.ufid_key))
        indv = models.Individual(grp_id_id=self.grp_id,
                                 spec_id=self.salmon_id,
                                 stok_id=self.stok_id,
                                 coll_id=self.coll_id,
                                 indv_year=year,
                                 pit_tag=row[self.pit_key],
                                 ufid=indv_ufid,
                                 indv_valid=True,
                                 comments=utils.nan_to_none(row[self.comment_key]),
                                 created_by=cleaned_data["created_by"],
                                 created_date=cleaned_data["created_date"],
                                 )
        try:
            indv.clean()
            indv.save()
            self.row_entered = True
        except (ValidationError, IntegrityError):
            indv = models.Individual.objects.filter(pit_tag=indv.pit_tag).get()

        if utils.nan_to_none(row[self.from_tank_key]) and utils.nan_to_none(row[self.to_tank_key]):
            in_tank = models.Tank.objects.filter(name=row[self.from_tank_key]).get()
            out_tank = models.Tank.objects.filter(name=row[self.to_tank_key]).get()
            self.row_entered += utils.create_movement_evnt(in_tank, out_tank, cleaned_data, row_datetime,
                                                      indv_pk=indv.pk)
            # if tagged fish goes back into same tank, still link fish to tank:
            if in_tank == out_tank:
                utils.enter_contx(in_tank, cleaned_data, True, indv_pk=indv.pk)

        anix_indv, anix_entered = utils.enter_anix(cleaned_data, indv_pk=indv.pk)
        self.row_entered += anix_entered
        self.anix_indv = anix_indv
        if utils.key_value_in_row(row, self.len_key_mm):
            self.row_entered += utils.enter_indvd(anix_indv.pk, cleaned_data, row_date, row[self.len_key_mm] / 10.0,
                                                  self.len_anidc_id.pk, None)
        if utils.key_value_in_row(row, self.len_key):
            self.row_entered += utils.enter_indvd(anix_indv.pk, cleaned_data, row_date, row[self.len_key],
                                                  self.len_anidc_id.pk, None)
        if utils.key_value_in_row(row, self.weight_key_kg):
            self.row_entered += utils.enter_indvd(anix_indv.pk, cleaned_data, row_date, 1000 * row[self.weight_key_kg],
                                                  self.weight_anidc_id.pk, None)
        if utils.key_value_in_row(row, self.weight_key):
            self.row_entered += utils.enter_indvd(anix_indv.pk, cleaned_data, row_date, row[self.weight_key],
                                                  self.weight_anidc_id.pk, None)
        if utils.key_value_in_row(row, self.vial_key):
            self.row_entered += utils.enter_indvd(anix_indv.pk, cleaned_data, row_date, row[self.vial_key],
                                                  self.vial_anidc_id.pk, None)
        if utils.key_value_in_row(row, self.precocity_key):
            self.row_entered += utils.enter_indvd(anix_indv.pk, cleaned_data, row_date, None,
                                                  self.ani_health_anidc_id.pk, "Precocity")

        if utils.key_value_in_row(row, self.crew_key):
            perc_list, inits_not_found = utils.team_list_splitter(row[self.crew_key])
            for perc_id in perc_list:
                team_id, team_entered = utils.add_team_member(perc_id, cleaned_data["evnt_id"],
                                                              role_id=self.tagger_code, return_team=True)
                self.row_entered += team_entered
                if team_id:
                    self.row_entered += utils.enter_anix(cleaned_data, indv_pk=indv.pk, team_pk=team_id.pk,
                                                         return_sucess=True)
            for inits in inits_not_found:
                self.log_data += "No valid personnel with initials ({}) for row with pit tag" \
                                 " {}\n".format(inits, row[self.pit_key])

        if utils.key_value_in_row(row, self.comment_key):
            comments_parsed, data_entered = utils.comment_parser(row[self.comment_key], anix_indv,
                                                                 det_date=row_datetime.date())
            self.row_entered += data_entered
            if not comments_parsed:
                self.log_data += "Unparsed comment on row with pit tag {}:\n {} \n\n".format(row[self.pit_key],
                                                                                             row[self.comment_key])

    def data_cleaner(self):
        from_tanks = self.data[self.from_tank_key].value_counts()
        for tank_name in from_tanks.keys():
            fish_tagged_from_tank = int(from_tanks[tank_name])
            contx, data_entered = utils.enter_tank_contx(tank_name, self.cleaned_data, None, grp_pk=self.grp_id,
                                                         return_contx=True)
            if contx:
                utils.enter_cnt(self.cleaned_data, fish_tagged_from_tank, contx.pk, cnt_code="Pit Tagged")


class MactaquacTaggingParser(TaggingParser):
    to_tank_key = "Destination Pond"
    from_tank_key = "Origin Pond"
    group_key = "Collection"
    pit_key = "PIT"
    vial_key = "Vial Number"
    crew_key = "Crew"

    header = 2
    converters = {to_tank_key: str, from_tank_key: str, pit_key: str, 'Year': str, 'Month': str, 'Day': str}

    def row_parser(self, row):
        super().row_parser(row)
        row_datetime = utils.get_row_date(row)


class ColdbrookTaggingParser(TaggingParser):
    box_key = "Box"
    location_key = "Location"
    precocity_key = "pp"
    indt_key = "Treatment"
    indt_amt_key = "Amount"

    box_anidc_id = None
    boxl_anidc_id = None

    def data_preper(self):
        super(ColdbrookTaggingParser, self).data_preper()
        self.box_anidc_id = models.AnimalDetCode.objects.filter(name="Box").get()
        self.boxl_anidc_id = models.AnimalDetCode.objects.filter(name="Box Location").get()

    def row_parser(self, row):
        super().row_parser(row)
        row_datetime = utils.get_row_date(row)
        row_date = row_datetime.date()
        if utils.key_value_in_row(row, self.box_key):
            self.row_entered += utils.enter_indvd(self.anix_indv.pk, self.cleaned_data, row_date, row[self.box_key],
                                                  self.box_anidc_id.pk, None)
        if utils.key_value_in_row(row, self.location_key):
            self.row_entered += utils.enter_indvd(self.anix_indv.pk, self.cleaned_data, row_date,
                                                  row[self.location_key], self.boxl_anidc_id.pk, None)

        if utils.key_value_in_row(row, self.indt_key) and utils.key_value_in_row(row, self.indt_amt_key):
            indvtc_id = models.IndTreatCode.objects.filter(name__icontains=row[self.indt_key]).get()
            unit_id = models.UnitCode.objects.filter(name__icontains="gram").order_by(Length('name').asc()).first()
            self.row_entered += utils.enter_indvt(self.anix_indv.pk, self.cleaned_data, row_datetime,
                                                  row[self.indt_amt_key], indvtc_id.pk, unit_id=unit_id)
