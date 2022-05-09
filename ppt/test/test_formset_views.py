from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate

from ..test import FactoryFloor
from ..test.common_tests import CommonProjectTest as CommonTest
from shared_models.views import CommonFormsetView, CommonHardDeleteView
from .. import views, utils
from .. import models
from faker import Factory

faker = Factory.create()


class TestAllFormsets(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url_names = [
            "manage_funding_sources",
            "manage_activity_types",
            "manage_om_cats",
            "manage_employee_types",
            "manage_tags",
            "manage_help_text",
            "manage_levels",
            "manage_themes",
            "manage-upcoming-dates",
            "manage_csrf_themes",
            "manage_csrf_sub_themes",
            "manage_csrf_priorities",
            "manage_csrf_client_information",
            "manage_services",
        ]

        self.test_urls = [reverse_lazy("ppt:" + name) for name in self.test_url_names]
        self.test_views = [
            views.FundingSourceFormsetView,
            views.ActivityTypeFormsetView,
            views.OMCategoryFormsetView,
            views.EmployeeTypeFormsetView,
            views.TagFormsetView,
            views.HelpTextFormsetView,
            views.LevelFormsetView,
            views.ThemeFormsetView,
            views.UpcomingDateFormsetView,
            views.CSRFThemeFormsetView,
            views.CSRFSubThemeFormsetView,
            views.CSRFPriorityFormsetView,
            views.CSRFClientInformationFormsetView,
            views.ServiceFormsetView,
        ]
        self.expected_template = 'ppt/formset.html'
        self.user = self.get_and_login_user(in_national_admin_group=True)

    @tag('formsets', "view")
    def test_view_class(self):
        for v in self.test_views:
            self.assert_inheritance(v, views.AdminRequiredMixin)
            self.assert_inheritance(v, CommonFormsetView)

    @tag('formsets', "access")
    def test_view(self):
        for url in self.test_urls:
            self.assert_good_response(url)
            self.assert_non_public_view(test_url=url, expected_template=self.expected_template, user=self.user)

    @tag('formsets', "submit")
    def test_submit(self):
        data = dict()  # should be fine to submit with empty data
        for url in self.test_urls:
            self.assert_success_url(url, data=data)


class TestAllHardDeleteViews(CommonTest):
    def setUp(self):
        super().setUp()
        self.starter_dicts = [
            {"model": models.FundingSource, "url_name": "delete_funding_source", "view": views.FundingSourceHardDeleteView},
            {"model": models.ActivityType, "url_name": "delete_activity_type", "view": views.ActivityTypeHardDeleteView},
            {"model": models.OMCategory, "url_name": "delete_om_cat", "view": views.OMCategoryHardDeleteView},
            {"model": models.EmployeeType, "url_name": "delete_employee_type", "view": views.EmployeeTypeHardDeleteView},
            {"model": models.Tag, "url_name": "delete_tag", "view": views.TagHardDeleteView},
            {"model": models.HelpText, "url_name": "delete_help_text", "view": views.HelpTextHardDeleteView},
            {"model": models.Level, "url_name": "delete_level", "view": views.LevelHardDeleteView},
            {"model": models.Theme, "url_name": "delete_theme", "view": views.ThemeHardDeleteView},
            {"model": models.UpcomingDate, "url_name": "delete-upcoming-date", "view": views.UpcomingDateHardDeleteView},
            {"model": models.CSRFTheme, "url_name": "delete_csrf_theme", "view": views.CSRFThemeHardDeleteView},
            {"model": models.CSRFSubTheme, "url_name": "delete_csrf_sub_theme", "view": views.CSRFSubThemeHardDeleteView},
            {"model": models.CSRFPriority, "url_name": "delete_csrf_priority", "view": views.CSRFPriorityHardDeleteView},
            {"model": models.CSRFClientInformation, "url_name": "delete_csrf_client_information", "view": views.CSRFClientInformationHardDeleteView},
            {"model": models.Service, "url_name": "delete_service", "view": views.ServiceHardDeleteView},
        ]
        self.test_dicts = list()

        self.user = self.get_and_login_user(in_national_admin_group=True)
        for d in self.starter_dicts:
            new_d = d
            m = d["model"]
            if m == models.FundingSource:
                obj = FactoryFloor.FundingSourceFactory()
            elif m == models.OMCategory:
                obj = m.objects.create(name=faker.word(), group=1)
            elif m == models.EmployeeType:
                obj = m.objects.create(name=faker.word(), cost_type=1)
            elif m == models.HelpText:
                obj = m.objects.create(field_name=faker.word(), eng_text=faker.word())
            elif m == models.UpcomingDate:
                obj = FactoryFloor.UpcomingDateFactory()

            elif m == models.CSRFTheme:
                obj = FactoryFloor.CSRFThemeFactory()
            elif m == models.CSRFSubTheme:
                obj = FactoryFloor.CSRFSubThemeFactory()
            elif m == models.CSRFPriority:
                obj = FactoryFloor.CSRFPriorityFactory()
            elif m == models.CSRFClientInformation:
                obj = FactoryFloor.CSRFClientInformationFactory()
            elif m == models.Service:
                obj = FactoryFloor.ServiceFactory()
            else:
                obj = m.objects.create(name=faker.word())
            new_d["obj"] = obj
            new_d["url"] = reverse_lazy("ppt:" + d["url_name"], kwargs={"pk": obj.id})
            self.test_dicts.append(new_d)

    @tag('hard_delete', "view")
    def test_view_class(self):
        for d in self.test_dicts:
            self.assert_inheritance(d["view"], views.AdminRequiredMixin)
            self.assert_inheritance(d["view"], CommonHardDeleteView)

    @tag('hard_delete', "access")
    def test_view(self):
        for d in self.test_dicts:
            self.assert_good_response(d["url"])
            # only have one chance to test this url
            self.assert_non_public_view(test_url=d["url"], user=self.user, expected_code=302, locales=["en"])

    @tag('hard_delete', "delete")
    def test_delete(self):
        # need to be an admin user to do this
        for d in self.test_dicts:
            # start off to confirm the object exists
            self.assertIn(d["obj"], type(d["obj"]).objects.all())
            # visit the url
            activate("en")
            response = self.client.get(d["url"])
            # confirm the object has been deleted
            self.assertNotIn(d["obj"], type(d["obj"]).objects.all())
