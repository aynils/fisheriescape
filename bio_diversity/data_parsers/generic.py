import copy
import pandas as pd

from bio_diversity import models
from bio_diversity import utils
from bio_diversity.static import calculation_constants


def parser_template(cleaned_data):
    log_data = "Loading Data Results: \n"
    rows_parsed = 0
    rows_entered = 0

    # loading data:
    try:
        data = pd.read_excel(cleaned_data["data_csv"], header=1, engine='openpyxl',
                             converters={'Year': str, 'Month': str, 'Day': str}).dropna(how="all")
        data_dict = data.to_dict('records')
    except Exception as err:
        log_data += "\n File format not valid: {}".format(err.__str__())
        return log_data, False

    # prepare rows before iterating:
    try:
        pass
    except Exception as err:
        err_msg = utils.common_err_parser(err)

        log_data += "\n Error preparing data: {}".format(err_msg)
        return log_data, False

    # iterate over rows
    for row in data_dict:
        row_entered = False
        try:
            pass
        except Exception as err:
            err_msg = utils.common_err_parser(err)

            log_data += "Error parsing row: \n"
            log_data += str(row)
            log_data += "\n Error: {}".format(err_msg)
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to" \
                        " database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))
            return log_data, False
        rows_parsed += 1
        if row_entered:
            rows_entered += 1

    # enter general data once all rows are entered:
    try:
        pass
    except Exception as err:
        err_msg = utils.common_err_parser(err)

        log_data += "Error parsing common data: \n"
        log_data += "\n Error: {}".format(err_msg)
        log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to" \
                    " database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))
        return log_data, False

    log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to" \
                " database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))
    return log_data, True


def generic_indv_parser(cleaned_data):
    log_data = "Loading Data Results: \n"
    rows_parsed = 0
    rows_entered = 0
    try:
        data = pd.read_excel(cleaned_data["data_csv"], engine='openpyxl', header=0,
                             converters={'PIT': str, 'Year': str, 'Month': str, 'Day': str}).dropna(how="all")
        data_dict = data.to_dict('records')
    except Exception as err:
        log_data += "\n File format not valid: {}".format(err.__str__())
        return log_data, False

    # data prep:
    sex_dict = calculation_constants.sex_dict

    for row in data_dict:
        row_entered = 0
        try:
            row_datetime = utils.get_row_date(row)
            row_date = row_datetime.date()

            indv_qs = models.Individual.objects.filter(pit_tag=row["PIT"])
            if len(indv_qs) == 1:
                indv = indv_qs.get()
            else:
                log_data += "Error parsing row: \n"
                log_data += str(row)
                log_data += "\nFish with PIT {} not found in db\n".format(row["PIT"])
                return log_data, False

            anix, anix_entered = utils.enter_anix(cleaned_data, indv_pk=indv.pk, return_sucess=True)
            row_entered += anix_entered

            if utils.nan_to_none(row["Sex"]):
                row_entered += utils.enter_indvd(anix.pk, cleaned_data, row_date, sex_dict[row["Sex"]], "Gender",
                                                 None, None)
            row_entered += utils.enter_indvd(anix.pk, cleaned_data, row_date, row["Length (cm)"], "Length", None)
            row_entered += utils.enter_indvd(anix.pk, cleaned_data, row_date, row["Weight (g)"], "Weight", None)
            row_entered += utils.enter_indvd(anix.pk, cleaned_data, row_date, row["Vial"], "Vial", None)
            row_entered += utils.enter_indvd(anix.pk, cleaned_data, row_date, row["Scale Envelope"], "Scale Envelope",
                                             None)
            if utils.y_n_to_bool(row["Precocity (Y/N)"]):
                row_entered += utils.enter_indvd(anix.pk, cleaned_data, row_date, None, "Animal Health",
                                                 "Tissue Sample")
            if utils.y_n_to_bool(row["Mortality (Y/N)"]):
                mort_evnt, mort_anix, mort_entered = utils.enter_mortality(indv, cleaned_data, row_date)
                row_entered += mort_entered
            if utils.y_n_to_bool(row["Tissue Sample (Y/N)"]):
                row_entered += utils.enter_indvd(anix.pk, cleaned_data, row_date, None, "Animal Health",
                                                 "Tissue Sample")

            if utils.nan_to_none(row["Origin Pond"]) and utils.nan_to_none(row["Destination Pond"]):
                in_tank = models.Tank.objects.filter(name=row["Origin Pond"]).get()
                out_tank = models.Tank.objects.filter(name=row["Destination Pond"]).get()
                row_entered += utils.create_movement_evnt(in_tank, out_tank, cleaned_data, row_datetime,
                                                          indv_pk=indv.pk)

            if utils.nan_to_none(row["COMMENTS"]):
                comments_parsed, data_entered = utils.comment_parser(row["COMMENTS"], anix, row_date)
                row_entered += data_entered
                if not comments_parsed:
                    log_data += "Unparsed comment on row with pit tag {}:\n {} \n\n".format(row["PIT"],
                                                                                            row["COMMENTS"])

        except Exception as err:
            err_msg = utils.common_err_parser(err)

            log_data += "Error parsing row: \n"
            log_data += str(row)
            log_data += "\n Error: {}".format(err_msg)
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))
            return log_data, False
        rows_parsed += 1
        if row_entered:
            rows_entered += 1

    log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))
    return log_data, True


def generic_grp_parser(cleaned_data):
    log_data = "Loading Data Results: \n"
    rows_parsed = 0
    rows_entered = 0
    try:
        data = pd.read_excel(cleaned_data["data_csv"], engine='openpyxl', header=0,
                             converters={'Year': str, 'Month': str, 'Day': str}).dropna(how="all")
    except Exception as err:
        log_data += "\n File format not valid: {}".format(err.__str__())
        return log_data, False

    # prep data:
    try:
        sex_dict = calculation_constants.sex_dict

        sampc_id = models.SampleCode.objects.filter(name="Individual Sample").get()

        # set date
        data["datetime"] = data.apply(lambda row: utils.get_row_date(row), axis=1)
        # split year-coll
        data["grp_year"] = data.apply(lambda row: utils.year_coll_splitter(row["Year Class"])[0], axis=1)
        data["grp_coll"] = data.apply(lambda row: utils.year_coll_splitter(row["Year Class"])[1], axis=1)

        # set start and end tanks:
        tank_qs = models.Tank.objects.filter(facic_id=cleaned_data["facic_id"])
        tank_dict = {tank.name: tank for tank in tank_qs}
        data["start_tank_id"] = data.apply(lambda row: tank_dict[row["Origin Pond"]], axis=1)
        data["end_tank_id"] = data.apply(lambda row: tank_dict[row["Destination Pond"]], axis=1)

        # set the dict keys for groups
        data["grp_key"] = data["River"] + data["Year Class"] + data["Origin Pond"] + data["Group"].astype(str) + \
                          data["datetime"].astype(str)

        data["end_grp_key"] = data["River"] + data["Year Class"] + data["Destination Pond"] + data["Group"].astype(str) + \
                              data["datetime"].astype(str)

        # create the start_grp dict and enter anixs:
        start_grp_data = data.groupby(["River", "grp_year", "grp_coll", "start_tank_id", "Group", "datetime", "grp_key"],
                                      dropna=False, sort=False).size().reset_index()
        start_grp_data["start_grp_id"] = start_grp_data.apply(
            lambda row: utils.get_grp(row["River"], row["grp_year"], row["grp_coll"],
                                      row["start_tank_id"], at_date=row["datetime"],
                                      prog_str=row["Group"], fail_on_not_found=True)[0], axis=1)
        start_grp_dict = dict(zip(start_grp_data['grp_key'], start_grp_data['start_grp_id']))
        for item, grp in start_grp_dict.items():
            utils.enter_anix(cleaned_data, grp_pk=grp.pk)

        # create the end group dict and create, movement event, groups, counts, contxs, etc. necesarry
        end_grp_data = data.groupby(
            ["River", "grp_year", "grp_coll", "end_tank_id", "start_tank_id", "Group", "datetime", "grp_key",
             "end_grp_key"],
            dropna=False, sort=False).size().reset_index()
        end_grp_dict = {}
        for row in end_grp_data.to_dict('records'):
            grps = utils.get_grp(row["River"], row["grp_year"], row["grp_coll"], row["end_tank_id"],
                                 at_date=row["datetime"],
                                 prog_str=row["Group"])
            start_grp_id = start_grp_dict[row["grp_key"]]
            start_contx = utils.enter_contx(row["start_tank_id"], cleaned_data, None, grp_pk=start_grp_id.pk,
                                            return_contx=True)
            utils.enter_cnt(cleaned_data, sum(end_grp_data[end_grp_data["grp_key"] == row["grp_key"]][0]),
                            start_contx.pk, cnt_code="Fish Removed from Container")

            if len(grps) > 0:
                end_grp_id = grps[0]
                end_grp_dict[row["end_grp_key"]] = grps[0]
            else:
                end_grp_id = copy.deepcopy(start_grp_id)
                end_grp_id.pk = None
                end_grp_id.save()
                end_grp_dict[row["end_grp_key"]] = end_grp_id

            grp_anix = utils.enter_anix(cleaned_data, grp_pk=end_grp_id.pk)
            utils.enter_grpd(grp_anix.pk, cleaned_data, row["datetime"], None, "Parent Group", frm_grp_id=start_grp_id)
            utils.enter_grpd(grp_anix.pk, cleaned_data, row["datetime"], None, "Program Group", row["Group"])
            end_contx = utils.create_movement_evnt(row["start_tank_id"], row["end_tank_id"], cleaned_data, row["datetime"],
                                                   grp_pk=end_grp_id.pk, return_end_contx=True)
            utils.enter_cnt(cleaned_data, row[0], end_contx.pk)
    except Exception as err:
        err_msg = utils.common_err_parser(err)
        log_data += "\n Error preparing data and finding initial groups: {}".format(err_msg)
        return log_data, False

    # iterate through the rows:
    data_dict = data.to_dict('records')
    for row in data_dict:
        row_entered = False
        try:
            row_date = row["datetime"].date()
            row_grp = start_grp_dict[row["grp_key"]]
            row_end_grp = end_grp_dict[row["end_grp_key"]]
            if row_end_grp:
                row_grp = row_end_grp
            row_anix, data_entered = utils.enter_anix(cleaned_data, grp_pk=row_grp.pk, return_sucess=True)
            row_entered += data_entered
            row_samp, data_entered = utils.enter_samp(cleaned_data, row["Sample"], row_grp.spec_id.pk, sampc_id.pk,
                                                      anix_pk=row_anix.pk )
            row_entered += data_entered

            if row_samp:
                if utils.nan_to_none(row["Sex"]):
                    row_entered += utils.enter_sampd(row_samp.pk, cleaned_data, row_date, sex_dict[row["Sex"]],
                                                     "Gender", None, None)
                row_entered += utils.enter_sampd(row_samp.pk, cleaned_data, row_date, row["Length (cm)"], "Length", None)
                row_entered += utils.enter_sampd(row_samp.pk, cleaned_data, row_date, row["Weight (g)"], "Weight", None)
                row_entered += utils.enter_sampd(row_samp.pk, cleaned_data, row_date, row["Vial"], "Vial", None)
                if utils.y_n_to_bool(row["Precocity (Y/N)"]):
                    row_entered += utils.enter_sampd(row_samp.pk, cleaned_data, row_date, None, "Animal Health",
                                                     "Tissue Sample")
                if utils.y_n_to_bool(row["Tissue Sample (Y/N)"]):
                    row_entered += utils.enter_sampd(row_samp.pk, cleaned_data, row_date, None, "Animal Health",
                                                     "Tissue Sample")

                row_entered += utils.enter_indvd(row_anix.pk, cleaned_data, row_date, row["Scale Envelope"],
                                                 "Scale Envelope", None)

                if utils.nan_to_none(row["COMMENTS"]):
                    comments_parsed, data_entered = utils.comment_parser(row["COMMENTS"], row_anix, row_date)
                    row_entered += data_entered
                    if not comments_parsed:
                        log_data += "Unparsed comment on row {}:\n {} \n\n".format(row, row["COMMENTS"])

            else:
                break

        except Exception as err:
            log_data += "Error parsing row: \n"
            log_data += str(row)
            log_data += "\n Error: {}".format(err.__str__())
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered,
                                                                           len(data_dict) )
            return log_data, False
        rows_parsed += 1
        if row_entered:
            rows_entered += 1

    log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))
    return log_data, True
