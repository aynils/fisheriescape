from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from shared_models.test.SharedModelsFactoryFloor import RegionFactory, CruiseFactory
from shared_models.views import CommonDeleteView, CommonPopoutDeleteView
from shared_models.models import Cruise
from cruises.test import FactoryFloor
from .. import models
from .. import views
from cruises.test.common_tests import CommonCruisesTest as CommonTest


class TestCruiseDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = CruiseFactory()
        self.test_url = reverse_lazy('cruises:cruise_delete', args=[self.instance.pk, ])
        self.expected_template = 'cruises/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="oceanography_admin")

    @tag("Cruise", "cruise_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.CruiseDeleteView, CommonDeleteView)

    @tag("Cruise", "cruise_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Cruise", "cruise_delete", "submit")
    def test_submit(self):
        data = CruiseFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(Cruise.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Cruise", "cruise_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("cruises:cruise_delete", f"/en/cruises/{self.instance.pk}/delete/", [self.instance.pk])


class TestFileDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FileFactory()
        self.test_url = reverse_lazy('cruises:file_delete', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="oceanography_admin")

    @tag("File", "file_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FileDeleteView, CommonPopoutDeleteView)

    @tag("File", "file_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("File", "file_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.FileFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.File.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("File", "file_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("cruises:file_delete", f"/en/cruises/file/{self.instance.pk}/delete/", [self.instance.pk])


class TestInstrumentDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.InstrumentFactory()
        self.test_url = reverse_lazy('cruises:instrument_delete', args=[self.instance.pk, ])
        self.expected_template = 'cruises/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="oceanography_admin")

    @tag("Instrument", "instrument_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.InstrumentDeleteView, CommonDeleteView)

    @tag("Instrument", "instrument_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Instrument", "instrument_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.InstrumentFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Instrument.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Instrument", "instrument_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("cruises:instrument_delete", f"/en/cruises/instrument/{self.instance.pk}/delete/", [self.instance.pk])


class TestInstrumentComponentDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.InstrumentComponentFactory()
        self.test_url = reverse_lazy('cruises:component_delete', args=[self.instance.pk, ])
        self.expected_template = 'cruises/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="oceanography_admin")

    @tag("InstrumentComponent", "component_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.InstrumentComponentDeleteView, CommonDeleteView)

    @tag("InstrumentComponent", "component_delete", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("InstrumentComponent", "component_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.InstrumentComponentFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.InstrumentComponent.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("InstrumentComponent", "component_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("cruises:component_delete", f"/en/cruises/component/{self.instance.pk}/delete/", [self.instance.pk])
