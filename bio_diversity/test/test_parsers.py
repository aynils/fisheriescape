
from django.contrib.staticfiles import finders
from django.test import tag

from django.utils import timezone

from bio_diversity import forms, models
from bio_diversity.data_parsers.calibration import CalibrationParser
from bio_diversity.data_parsers.distributions import DistributionIndvParser
from bio_diversity.data_parsers.electrofishing import MactaquacElectrofishingParser, ColdbrookElectrofishingParser
from bio_diversity.data_parsers.generic import GenericUntaggedParser, GenericIndvParser, GenericGrpParser
from bio_diversity.data_parsers.master import MasterIndvParser, MasterGrpParser
from bio_diversity.data_parsers.tagging import MactaquacTaggingParser, ColdbrookTaggingParser
from bio_diversity.data_parsers.treatment import MactaquacTreatmentParser
from bio_diversity.data_parsers.water_quality import WaterQualityParser
from bio_diversity.test import BioFactoryFloor
from shared_models.test.common_tests import CommonTest
from bio_diversity.models import PersonnelCode, Pairing, Program, Individual


@tag("Electrofishing", 'Parser')
class TestMactaquacParsers(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures
        mactaquac_facic = models.FacilityCode.objects.filter(name="Mactaquac").get()
        self.electrofishing_evntc = models.EventCode.objects.filter(name="Electrofishing").get()
        self.tagging_evntc = models.EventCode.objects.filter(name="PIT Tagging").get()
        self.measuring_evntc = models.EventCode.objects.filter(name="Measuring").get()
        self.dist_evntc = models.EventCode.objects.filter(name="Distribution").get()

        # used to get the full path from the static directory
        self.electrofishing_test_data = finders.find("test\\parser_test_files\\test-electrofishing.xlsx")
        self.tagging_test_data = finders.find("test\\parser_test_files\\test-tagging.xlsx")
        self.measuring_test_data = finders.find("test\\parser_test_files\\test-generic-group.xlsx")
        self.measuring_indv_test_data = finders.find("test\\parser_test_files\\test-generic-indv.xlsx")
        self.dist_indv_test_data = finders.find("test\\parser_test_files\\test-indv-distribution.xlsx")

        self.electrofishing_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.electrofishing_evntc, facic_id=mactaquac_facic)
        self.tagging_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.tagging_evntc, facic_id=mactaquac_facic)
        self.measuring_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.measuring_evntc, facic_id=mactaquac_facic)
        self.grp_measuring_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.measuring_evntc, facic_id=mactaquac_facic)
        self.dist_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.dist_evntc, facic_id=mactaquac_facic)

        self.cleaned_data = {
            "facic_id": mactaquac_facic,
            "evnt_id": self.electrofishing_evnt,
            "evntc_id": self.electrofishing_evntc,
            "adsc_id": [],
            "anidc_id": [],
            "anidc_subj_id": [],
            "data_csv": self.electrofishing_test_data,
            "created_by": self.electrofishing_evnt.created_by,
            "created_date": self.electrofishing_evnt.created_date,
        }

    def test_parser(self):
        # assertingTrue on the parser result is to avoid errors raised and caught in the parsers.
        # If the parsers crash, they will return success = False as well as log data of the error
        parser = MactaquacElectrofishingParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

        # Tagging parser
        self.cleaned_data["evnt_id"] = self.tagging_evnt
        self.cleaned_data["evntc_id"] = self.tagging_evntc
        self.cleaned_data["data_csv"] = self.tagging_test_data
        parser = MactaquacTaggingParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

        # Generic Untagged Parser
        self.cleaned_data["evnt_id"] = self.measuring_evnt
        self.cleaned_data["evntc_id"] = self.measuring_evntc
        self.cleaned_data["data_csv"] = self.measuring_test_data
        parser = GenericUntaggedParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

        # Generic Group Parser
        self.cleaned_data["evnt_id"] = self.grp_measuring_evnt
        self.cleaned_data["evntc_id"] = self.measuring_evntc
        self.cleaned_data["data_csv"] = self.measuring_test_data
        parser = GenericGrpParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

        # Generic Individual parser
        self.cleaned_data["data_csv"] = self.measuring_indv_test_data
        parser = GenericIndvParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

        # Distirbution Individual parser
        self.cleaned_data["evnt_id"] = self.dist_evnt
        self.cleaned_data["evntc_id"] = self.dist_evntc
        self.cleaned_data["data_csv"] = self.dist_indv_test_data
        parser = DistributionIndvParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)


@tag("Electrofishing", 'Parser')
class TestColdbrookParsers(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures
        coldbrook_facic = models.FacilityCode.objects.filter(name="Coldbrook").get()
        self.electrofishing_evntc = models.EventCode.objects.filter(name="Electrofishing").get()
        self.tagging_evntc = models.EventCode.objects.filter(name="PIT Tagging").get()
        self.measuring_evntc = models.EventCode.objects.filter(name="Measuring").get()
        self.dist_evntc = models.EventCode.objects.filter(name="Distribution").get()

        # used to get the full path from the static directory
        self.electrofishing_test_data = finders.find("test\\parser_test_files\\test-electrofishing-cb.xlsx")
        self.tagging_test_data = finders.find("test\\parser_test_files\\test-tagging-cb.xlsx")

        self.electrofishing_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.electrofishing_evntc, facic_id=coldbrook_facic)
        self.tagging_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.tagging_evntc, facic_id=coldbrook_facic)

        self.cleaned_data = {
            "facic_id": coldbrook_facic,
            "evnt_id": self.electrofishing_evnt,
            "evntc_id": self.electrofishing_evntc,
            "data_csv": self.electrofishing_test_data,
            "created_by": self.electrofishing_evnt.created_by,
            "created_date": self.electrofishing_evnt.created_date,
        }

    def test_parser(self):
        # this is to ignore all of the errors raised and caught in the parsers.  If the parsers crash, they will return
        # success = False as well as log data of the error
        parser = ColdbrookElectrofishingParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)
        self.assertEqual(parser.rows_entered, 3)

        # Tagging parser
        self.cleaned_data["evnt_id"] = self.tagging_evnt
        self.cleaned_data["evntc_id"] = self.tagging_evntc
        self.cleaned_data["data_csv"] = self.tagging_test_data
        parser = ColdbrookTaggingParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)


@tag("Master", 'Parser')
class TestMasterParser(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures
        mactaquac_facic = models.FacilityCode.objects.filter(name="Mactaquac").get()
        self.master_entry_evntc = models.EventCode.objects.filter(name="Master Entry").get()

        # used to get the full path from the static directory
        self.master_entry_test_data = finders.find("test\\parser_test_files\\test-master_entry.xlsx")

        self.master_entry_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.master_entry_evntc, facic_id=mactaquac_facic)

        self.cleaned_data = {
            "facic_id": mactaquac_facic,
            "evnt_id": self.master_entry_evnt,
            "evntc_id": self.master_entry_evntc,
            "data_csv": self.master_entry_test_data,
            "created_by": self.master_entry_evnt.created_by,
            "created_date": self.master_entry_evnt.created_date,
        }

    def test_indv_parser(self):
        # this is to ignore all of the errors raised and caught in the parsers.  If the parsers crash, they will return
        # success = False as well as log data of the error
        parser = MasterIndvParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

    def test_grp_parser(self):
        # this is to ignore all of the errors raised and caught in the parsers.  If the parsers crash, they will return
        # success = False as well as log data of the error
        parser = MasterGrpParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

@tag("Calibration", 'Parser')
class TestCalibrationParser(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures
        self.mactaquac_facic = models.FacilityCode.objects.filter(name="Mactaquac").get()
        self.calibration_evntc = models.EventCode.objects.filter(name="Calibration").get()

        # used to get the full path from the static directory
        self.calibration_test_data = finders.find("test\\parser_test_files\\test-calibration.xlsx")

        self.calibration_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.calibration_evntc, facic_id=self.mactaquac_facic,
                                                            start_datetime=timezone.now(), created_date=timezone.now(),
                                                            end_datetime=None)

        self.cleaned_data = {
            "facic_id": self.mactaquac_facic,
            "evnt_id": self.calibration_evnt,
            "evntc_id": self.calibration_evntc,
            "data_csv": self.calibration_test_data,
            "created_by": self.calibration_evnt.created_by,
            "created_date": self.calibration_evnt.created_date,
        }

    def test_calibration_parser(self):
        # this is to ignore all of the errors raised and caught in the parsers.  If the parsers crash, they will return
        # success = False as well as log data of the error
        grp_a = BioFactoryFloor.GrpFactory()
        grp_b = BioFactoryFloor.GrpFactory()
        grp_c = BioFactoryFloor.GrpFactory()
        tank_a = BioFactoryFloor.TankFactory(name="Tank A", facic_id=self.mactaquac_facic)

        # set pk's to match test parser sheet
        grp_a.pk = 7777
        grp_a.save()
        grp_b.pk = 8888
        grp_b.save()
        grp_c.pk = 9999
        grp_c.save()

        parser = CalibrationParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)

        # refresh grps
        grp_a = models.Group.objects.filter(pk=grp_a.pk).get()
        grp_b = models.Group.objects.filter(pk=grp_b.pk).get()
        grp_c = models.Group.objects.filter(pk=grp_c.pk).get()
        self.assertEqual(grp_a.count_fish_in_group(at_date=timezone.now()), 7777)
        self.assertEqual(grp_a.grp_end_date, self.calibration_evnt.start_datetime.date())
        self.assertIn(grp_b, tank_a.fish_in_cont()[1])
        self.assertEqual(grp_c.grp_valid, False)


@tag("Treatment", 'Parser')
class TestTreatmentParser(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures
        mactaquac_facic = models.FacilityCode.objects.filter(name="Mactaquac").get()
        self.treatment_evntc = models.EventCode.objects.filter(name="Treatment").get()

        # used to get the full path from the static directory
        self.treatment_test_data = finders.find("test\\parser_test_files\\test-treatment.xlsx")

        self.treatment_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.treatment_evntc, facic_id=mactaquac_facic)

        self.cleaned_data = {
            "facic_id": mactaquac_facic,
            "evnt_id": self.treatment_evnt,
            "evntc_id": self.treatment_evntc,
            "data_csv": self.treatment_test_data,
            "created_by": self.treatment_evnt.created_by,
            "created_date": self.treatment_evnt.created_date,
        }

    def test_parser(self):
        # this is to ignore all of the errors raised and caught in the parsers.  If the parsers crash, they will return
        # success = False as well as log data of the error
        parser = MactaquacTreatmentParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)


@tag("WaterQuality", 'Parser')
class TestWaterQualityReportParser(CommonTest):
    fixtures = ["initial_data.json"]

    def setUp(self):
        super().setUp()  # used to import fixtures
        mactaquac_facic = models.FacilityCode.objects.filter(name="Mactaquac").get()
        self.water_quality_evntc = models.EventCode.objects.filter(name="Water Quality Record").get()

        # used to get the full path from the static directory
        self.water_qaulity_test_data = finders.find("test\\parser_test_files\\test-water_quality_record.xlsx")

        self.water_quality_evnt = BioFactoryFloor.EvntFactory(evntc_id=self.water_quality_evntc, facic_id=mactaquac_facic)

        self.cleaned_data = {
            "facic_id": mactaquac_facic,
            "evnt_id": self.water_quality_evnt,
            "evntc_id": self.water_quality_evntc,
            "data_csv": self.water_qaulity_test_data,
            "created_by": self.water_quality_evnt.created_by,
            "created_date": self.water_quality_evnt.created_date,
        }

    def test_parser(self):
        # this is to ignore all of the errors raised and caught in the parsers.  If the parsers crash, they will return
        # success = False as well as log data of the error
        parser = WaterQualityParser(self.cleaned_data)
        self.assertTrue(parser.success, parser.log_data)
