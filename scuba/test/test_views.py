from django.shortcuts import get_object_or_404
from django.test import tag
from django.urls import reverse_lazy
from faker import Factory

from shared_models.utils import dm2decdeg
from shared_models.views import CommonCreateView, CommonFilterView, CommonUpdateView, CommonDeleteView, CommonDetailView, CommonFormView
from . import FactoryFloor
from .FactoryFloor import DiveFactory
from .common_tests import ScubaCommonTest as CommonTest
from .. import views, models

faker = Factory.create()


class TestDiveCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SampleFactory()
        self.test_url = reverse_lazy('scuba:dive_new', args=[self.instance.id])
        self.expected_template = 'scuba/form.html'
        self.user = self.get_and_login_admin()

    @tag("Dive", "dive_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.DiveCreateView, CommonCreateView)

    @tag("Dive", "dive_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Dive", "dive_new", "submit")
    def test_submit(self):
        data = FactoryFloor.DiveFactory.get_valid_data(self.instance)
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Dive", "dive_new", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:dive_new", f"/en/scuba/samples/{self.instance.pk}/new-dive/", [self.instance.pk])


class TestDiveDataEntryDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DiveFactory()
        self.test_url = reverse_lazy('scuba:dive_data_entry', args=[self.instance.pk, ])
        self.expected_template = 'scuba/dive_data_entry/main.html'
        self.user = self.get_and_login_admin()

    @tag("Dive", "dive_data_entry", "view")
    def test_view_class(self):
        self.assert_inheritance(views.DiveDetailView, CommonDetailView)

    @tag("Dive", "dive_data_entry", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Dive", "dive_data_entry", "context")
    def test_context(self):
        context_vars = [
            "section_field_list",
            "random_section",
            "observation_field_list",
            "random_observation",
            "section_form",
            "obs_form",
            "new_obs_form",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Dive", "dive_data_entry", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:dive_data_entry", f"/en/scuba/dives/{self.instance.pk}/data-entry/", [self.instance.pk])


class TestDiveDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DiveFactory()
        self.test_url = reverse_lazy('scuba:dive_delete', args=[self.instance.pk, ])
        self.expected_template = 'scuba/confirm_delete.html'
        self.user = self.get_and_login_admin()

    @tag("Dive", "dive_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.DiveDeleteView, CommonDeleteView)

    @tag("Dive", "dive_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Dive", "dive_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.DiveFactory.get_valid_data(self.instance.sample)
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Dive.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Dive", "dive_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:dive_delete", f"/en/scuba/dives/{self.instance.pk}/delete/", [self.instance.pk])


class TestDiveDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DiveFactory()
        self.test_url = reverse_lazy('scuba:dive_detail', args=[self.instance.pk, ])
        self.expected_template = 'scuba/dive_detail.html'
        self.user = self.get_and_login_admin()

    @tag("Dive", "dive_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.DiveDetailView, CommonDetailView)

    @tag("Dive", "dive_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Dive", "dive_detail", "context")
    def test_context(self):
        context_vars = [
            "section_field_list",
            "observation_field_list",
            "random_observation",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Dive", "dive_detail", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:dive_detail", f"/en/scuba/dives/{self.instance.pk}/view/", [self.instance.pk])


class TestDiveLogReportView(CommonTest):
    def setUp(self):
        super().setUp()
        DiveFactory()
        DiveFactory()
        DiveFactory()
        DiveFactory()
        self.test_url = reverse_lazy('scuba:dive_log_report')
        self.user = self.get_and_login_admin()

    @tag("DiveLog", "dive_log_report", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, user=self.user)

    @tag("DiveLog", "dive_log_report", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:dive_log_report", f"/en/scuba/reports/dive-log/")


class TestDiveUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DiveFactory()
        self.test_url = reverse_lazy('scuba:dive_edit', args=[self.instance.pk, ])
        self.expected_template = 'scuba/form.html'
        self.user = self.get_and_login_admin()

    @tag("Dive", "dive_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.DiveUpdateView, CommonUpdateView)

    @tag("Dive", "dive_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Dive", "dive_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.DiveFactory.get_valid_data(self.instance.sample)
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Dive", "dive_edit", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:dive_edit", f"/en/scuba/dives/{self.instance.pk}/edit/", [self.instance.pk])


class TestRegionCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('scuba:region_new')
        self.expected_template = 'scuba/form.html'
        self.user = self.get_and_login_admin()

    @tag("Region", "region_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionCreateView, CommonCreateView)

    @tag("Region", "region_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Region", "region_new", "submit")
    def test_submit(self):
        data = FactoryFloor.RegionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Region", "region_new", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:region_new", f"/en/scuba/regions/new/")


class TestRegionDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RegionFactory()
        self.test_url = reverse_lazy('scuba:region_delete', args=[self.instance.pk, ])
        self.expected_template = 'scuba/confirm_delete.html'
        self.user = self.get_and_login_admin()

    @tag("Region", "region_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionDeleteView, CommonDeleteView)

    @tag("Region", "region_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Region", "region_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.RegionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Region.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Region", "region_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:region_delete", f"/en/scuba/regions/{self.instance.pk}/delete/", [self.instance.pk])


class TestRegionDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RegionFactory()
        self.test_url = reverse_lazy('scuba:region_detail', args=[self.instance.pk, ])
        self.expected_template = 'scuba/region_detail.html'
        self.user = self.get_and_login_admin()

    @tag("Region", "region_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionDetailView, CommonDetailView)

    @tag("Region", "region_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Region", "region_detail", "context")
    def test_context(self):
        context_vars = [
            "transect_field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Region", "region_detail", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:region_detail", f"/en/scuba/regions/{self.instance.pk}/view/", [self.instance.pk])


class TestRegionListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('scuba:region_list')
        self.expected_template = 'scuba/list.html'
        self.user = self.get_and_login_admin()

    @tag("Region", "region_list", "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionListView, CommonFilterView)

    @tag("Region", "region_list", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Region", "region_list", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Region", "region_list", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:region_list", f"/en/scuba/regions/")


class TestRegionUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RegionFactory()
        self.test_url = reverse_lazy('scuba:region_edit', args=[self.instance.pk, ])
        self.expected_template = 'scuba/form.html'
        self.user = self.get_and_login_admin()

    @tag("Region", "region_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.RegionUpdateView, CommonUpdateView)

    @tag("Region", "region_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Region", "region_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.RegionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Region", "region_edit", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:region_edit", f"/en/scuba/regions/{self.instance.pk}/edit/", [self.instance.pk])


class TestReportSearchFormView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('scuba:reports')
        self.expected_template = 'scuba/report_search.html'
        self.user = self.get_and_login_admin()

    @tag("ReportSearch", "reports", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ReportSearchFormView, CommonFormView)

    @tag("ReportSearch", "reports", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("ReportSearch", "reports", "submit")
    def test_submit(self):
        data = dict(report=1)
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("ReportSearch", "reports", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:reports", f"/en/scuba/reports/")


class TestSampleCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('scuba:sample_new')
        self.expected_template = 'scuba/coord_form.html'
        self.user = self.get_and_login_admin()

    @tag("Sample", "sample_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SampleCreateView, CommonCreateView)

    @tag("Sample", "sample_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Sample", "sample_new", "submit")
    def test_submit(self):
        data = FactoryFloor.SampleFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Sample", "sample_new", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:sample_new", f"/en/scuba/samples/new/")


class TestSampleDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SampleFactory()
        self.test_url = reverse_lazy('scuba:sample_delete', args=[self.instance.pk, ])
        self.expected_template = 'scuba/confirm_delete.html'
        self.user = self.get_and_login_admin()

    @tag("Sample", "sample_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SampleDeleteView, CommonDeleteView)

    @tag("Sample", "sample_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Sample", "sample_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.SampleFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Sample.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Sample", "sample_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:sample_delete", f"/en/scuba/samples/{self.instance.pk}/delete/", [self.instance.pk])


class TestSampleDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SampleFactory()
        self.test_url = reverse_lazy('scuba:sample_detail', args=[self.instance.pk, ])
        self.expected_template = 'scuba/sample_detail.html'
        self.user = self.get_and_login_admin()

    @tag("Sample", "sample_detail", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SampleDetailView, CommonDetailView)

    @tag("Sample", "sample_detail", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Sample", "sample_detail", "context")
    def test_context(self):
        context_vars = [
            "dive_field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Sample", "sample_detail", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:sample_detail", f"/en/scuba/samples/{self.instance.pk}/view/", [self.instance.pk])


class TestSampleListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('scuba:sample_list')
        self.expected_template = 'scuba/list.html'
        self.user = self.get_and_login_admin()

    @tag("Sample", "sample_list", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SampleListView, CommonFilterView)

    @tag("Sample", "sample_list", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Sample", "sample_list", "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Sample", "sample_list", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:sample_list", f"/en/scuba/samples/")


class TestSampleUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SampleFactory()
        self.test_url = reverse_lazy('scuba:sample_edit', args=[self.instance.pk, ])
        self.expected_template = 'scuba/coord_form.html'
        self.user = self.get_and_login_admin()

    @tag("Sample", "sample_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SampleUpdateView, CommonUpdateView)

    @tag("Sample", "sample_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Sample", "sample_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.SampleFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Sample", "sample_edit", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:sample_edit", f"/en/scuba/samples/{self.instance.pk}/edit/", [self.instance.pk])


class TestTransectCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RegionFactory()
        self.test_url = reverse_lazy('scuba:transect_new', args=[self.instance.id])
        self.expected_template = 'scuba/coord_form.html'
        self.user = self.get_and_login_admin()

    @tag("Transect", "transect_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransectCreateView, CommonCreateView)

    @tag("Transect", "transect_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Transect", "transect_new", "submit")
    def test_submit(self):
        data = FactoryFloor.TransectFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Transect", "transect_new", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:transect_new", f"/en/scuba/regions/{self.instance.id}/new-transect/", test_url_args=[self.instance.id])


class TestTransectDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransectFactory()
        self.test_url = reverse_lazy('scuba:transect_delete', args=[self.instance.pk, ])
        self.expected_template = 'scuba/confirm_delete.html'
        self.user = self.get_and_login_admin()

    @tag("Transect", "transect_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransectDeleteView, CommonDeleteView)

    @tag("Transect", "transect_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Transect", "transect_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.TransectFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Transect.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Transect", "transect_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:transect_delete", f"/en/scuba/transects/{self.instance.pk}/delete/", [self.instance.pk])


class TestTransectUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransectFactory()
        self.test_url = reverse_lazy('scuba:transect_edit', args=[self.instance.pk, ])
        self.expected_template = 'scuba/coord_form.html'
        self.user = self.get_and_login_admin()

    @tag("Transect", "transect_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransectUpdateView, CommonUpdateView)

    @tag("Transect", "transect_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Transect", "transect_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.TransectFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # let's test out the save method
        data = FactoryFloor.TransectFactory.get_valid_data()
        data['start_latitude_d'] = 48
        data['start_latitude_mm'] = 12.34
        data['start_longitude_d'] = -64
        data['start_longitude_mm'] = 56.78
        data['end_latitude_d'] = 49
        data['end_latitude_mm'] = 13.34
        data['end_longitude_d'] = -65
        data['end_longitude_mm'] = 57.78
        self.assert_success_url(self.test_url, data=data, user=self.user)

        obj = get_object_or_404(models.Transect, pk=self.instance.pk)
        self.assertEqual(dm2decdeg(data['start_latitude_d'], data['start_latitude_mm']), obj.start_latitude)
        self.assertEqual(dm2decdeg(data['start_longitude_d'], data['start_longitude_mm']), obj.start_longitude)
        self.assertEqual(dm2decdeg(data['end_latitude_d'], data['end_latitude_mm']), obj.end_latitude)
        self.assertEqual(dm2decdeg(data['end_longitude_d'], data['end_longitude_mm']), obj.end_longitude)

    @tag("Transect", "transect_edit", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("scuba:transect_edit", f"/en/scuba/transects/{self.instance.pk}/edit/", [self.instance.pk])
