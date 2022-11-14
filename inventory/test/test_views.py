from django.test import tag
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DetailView, ListView, DeleteView, CreateView
from django_filters.views import FilterView
from easy_pdf.views import PDFTemplateView

from inventory.test import FactoryFloor
from inventory.test.common_tests import CommonInventoryTest as CommonTest
from .. import views, models


class TestIndexTemplateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:index')
        self.expected_template = 'inventory/index.html'

    @tag("inventory", 'index', "view")
    def test_view_class(self):
        self.assert_inheritance(views.Index, TemplateView)

    @tag("inventory", 'index', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)


class TestMyResourceListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:my_resource_list')
        self.expected_template = 'inventory/resource_list.html'

    @tag("inventory", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.MyResourceListView, ListView)

    @tag("inventory", 'list', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)


class TestOpenDataDashboardTemplateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:open_data_dashboard')
        self.expected_template = 'inventory/open_data_dashboard.html'

    @tag("inventory", 'open_data', "view")
    def test_view_class(self):
        self.assert_inheritance(views.OpenDataDashboardTemplateView, TemplateView)

    @tag("inventory", 'open_data', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    @tag("inventory", 'open_data', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "my_dict",
            "current_fy",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)


class TestResourceCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:resource_new')
        self.expected_template = 'inventory/resource_form.html'

    @tag("inventory", 'create', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceCreateView, CreateView)

    @tag("inventory", 'create', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("inventory", 'create', "context")
    def test_context(self):
        context_vars = [
            "resource_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

    @tag("inventory", 'create', "submit")
    def test_submit(self):
        data = FactoryFloor.ResourceFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data)
        # get the instance just created and ensure there is a uuid
        my_instance = models.Resource.objects.get(**data)
        self.assertIsNotNone(my_instance.uuid)


class TestResourceDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.user = self.get_and_login_user(is_admin=True)
        self.test_url = reverse_lazy('inventory:resource_delete', kwargs={"pk": self.instance.pk})
        self.expected_template = 'inventory/confirm_delete.html'

    @tag("inventory", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceDeleteView, DeleteView)

    @tag("inventory", 'delete', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        test_user = self.get_and_login_user()
        self.assert_user_access_denied(test_url=self.test_url, user=test_user, login_search_term="accounts/denied")

    @tag("inventory", 'delete', "submit")
    def test_submit(self):
        self.assert_success_url(self.test_url, user=self.user)
        # for delete views...
        self.assertEqual(models.Resource.objects.filter(pk=self.instance.pk).count(), 0)


class TestResourceDetailPDFView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.test_url = reverse_lazy('inventory:resource_pdf', args=[self.instance.pk])
        self.expected_template = 'inventory/resource_detail_pdf.html'

    @tag("resource_pdf", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceDetailPDFView, PDFTemplateView)

    @tag("resource_pdf", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)

    @tag("resource_pdf", "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "now",
            "object",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)


# class TestResourceDetailView(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.resource = FactoryFloor.ResourceFactory()
#         self.test_url = reverse_lazy('inventory:resource_detail', kwargs={"pk": self.resource.pk})
#         self.expected_template = 'inventory/resource_detail.html'
#
#     @tag("inventory", 'detail', "view")
#     def test_view_class(self):
#         self.assert_inheritance(views.ResourceDetailView, DetailView)
#
#     @tag("inventory", 'detail', "access")
#     def test_view(self):
#         self.assert_good_response(self.test_url)
#         self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)


class TestResourceListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('inventory:resource_list')
        self.expected_template = 'inventory/resource_list.html'

    @tag("inventory", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceListView, FilterView)

    @tag("inventory", 'list', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        # create an admin user (who should always be able to delete) and check to see there is a 200 response
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("inventory", 'list', "context")
    def test_context(self):
        context_vars = [
            "object_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)


class TestResourceUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.test_url = reverse_lazy('inventory:resource_edit', kwargs={"pk": self.instance.pk})
        self.resource_person = FactoryFloor.CustodianResourcePersonFactory(resource=self.instance)
        self.expected_template = 'inventory/resource_form.html'

    @tag("inventory", 'update', "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceUpdateView, UpdateView)

    @tag("inventory", 'update', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        # the user must be a custodian...
        user = FactoryFloor.CustodianResourcePersonFactory(resource=self.instance)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.resource_person.person.user)

    @tag("inventory", 'update', "submit")
    def test_submit(self):
        data = FactoryFloor.ResourceFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.resource_person.person.user)


class TestResourceCloneUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.test_url = reverse_lazy('inventory:resource_clone', args=[self.instance.pk, ])
        self.expected_template = 'inventory/resource_form.html'
        self.user = self.get_and_login_user()

    @tag("Resource", "resource_clone", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResourceCloneUpdateView, views.ResourceUpdateView)

    @tag("Resource", "resource_clone", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Resource", "resource_clone", "context")
    def test_context(self):
        context_vars = [
            "cloning",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("Resource", "resource_clone", "submit")
    def test_submit(self):
        data = FactoryFloor.ResourceFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Resource", "resource_clone", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("inventory:resource_clone", f"/en/inventory/resources/{self.instance.pk}/clone/", [self.instance.pk])


class TestResourceXMLExport(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResourceFactory()
        self.test_url1 = reverse_lazy('inventory:export_xml',
                                      kwargs={"resource": self.instance.pk, "publish": "no"})  # this will be a draft
        self.test_url2 = reverse_lazy('inventory:export_xml',
                                      kwargs={"resource": self.instance.pk, "publish": "yes"})  # this will be to publish

    @tag("xml_export", 'update', "access")
    def test_xml_export_function(self):
        # let's ensure the resource starts out without a fgp date or revision date
        self.assertIsNone(self.instance.fgp_publication_date)
        self.assertIsNone(self.instance.last_revision_date)

        self.assert_good_response(self.test_url1)
        self.assert_public_view(test_url=self.test_url1)

        # update the instance to check to see if fields were updated. they should not be
        self.instance = models.Resource.objects.get(pk=self.instance.pk)
        # this resource should not have an fgp publication date
        self.assertIsNone(self.instance.fgp_publication_date)
        self.assertIsNone(self.instance.last_revision_date)

        # check the second url
        response = self.client.get(self.test_url2)
        self.instance = models.Resource.objects.get(pk=self.instance.pk)
        self.assertIsNotNone(self.instance.fgp_publication_date)
        self.assertIsNone(self.instance.last_revision_date)

        # run a second time, the url2 should populate the last_revision_date
        response = self.client.get(self.test_url2)
        self.instance = models.Resource.objects.get(pk=self.instance.pk)
        self.assertIsNotNone(self.instance.fgp_publication_date)
        self.assertIsNotNone(self.instance.last_revision_date)
