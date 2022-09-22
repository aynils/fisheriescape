from django.test import tag, RequestFactory
from django.urls import reverse_lazy
from faker import Faker
from datetime import date

from bio_diversity.test import BioFactoryFloor
from shared_models.test.common_tests import CommonTest

from bio_diversity.views import CommonCreate, CommonDetails, CommonUpdate, GenericList
from shares.models import User
from .. import views
from ..models import BioUser

faker = Faker()


# This is used to simulate calling the as_veiw() function normally called in the urls.py
# this will return a view that can then have it's internal methods tested
def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class CommonBioTest(CommonTest):

    # use when an admin user needs to be logged in.
    def login_bio_admin_user(self):
        user = self.get_and_login_user()
        BioUser(user=user, is_admin=True).save()
        return user

    # use when an author user needs to be logged in.
    def login_bio_author_user(self):
        user = self.get_and_login_user()
        BioUser(user=user, is_author=True).save()
        return user


class MockCommonCreate(views.CommonCreate):
    pass


@tag('CreateCommon')
class TestCommonCreate(CommonBioTest):

    def setUp(self):
        self.view = MockCommonCreate()

    def test_get_init(self):
        # test created_by field auto population
        req_faq = RequestFactory()
        request = req_faq.get(None)

        # create and login a user to be expected by the inital function
        user = self.login_bio_admin_user()
        request.user = user

        setup_view(self.view, request)

        init = self.view.get_initial()
        self.assertIsNotNone(init)
        self.assertEqual(init['created_by'], user.username)
        self.assertEqual(init['created_by'], user.username)
        self.assertEqual(init['created_date'], date.today)


@tag("Anidc")
class TestAnidcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnidcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_anidc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnidcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AnidcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_anidc", "/en/bio_diversity/create/anidc/")


@tag("Anidc")
class TestAnidcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnidcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_anidc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnidcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "min_val",
            "max_val",
            "unit_id",
            "ani_subj_flag",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_anidc", f"/en/bio_diversity/details/anidc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Anidc")
class TestAnidcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_anidc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnidcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_anidc", f"/en/bio_diversity/list/anidc/")


@tag("Anidc")
class AnidcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnidcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_anidc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnidcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AnidcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_anidc", f"/en/bio_diversity/update/anidc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Anix")
class TestAnixCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnixFactory()
        self.test_url = reverse_lazy('bio_diversity:create_anix')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnixCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AnixFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_anix", "/en/bio_diversity/create/anix/")


@tag("Anix")
class TestAnixDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnixFactory()
        self.test_url = reverse_lazy('bio_diversity:details_anix', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnixDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "evnt_id",
            "loc_id",
            "indv_id",
            "pair_id",
            "grp_id",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_anix", f"/en/bio_diversity/details/anix/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Anix")
class TestAnixListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_anix')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnixList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_anix", f"/en/bio_diversity/list/anix/")


@tag("Anix")
class AnixUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AnixFactory()
        self.test_url = reverse_lazy('bio_diversity:update_anix', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.AnixUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AnixFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_anix", f"/en/bio_diversity/update/anix/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Adsc")
class TestAdscCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AdscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_adsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.AdscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_adsc", "/en/bio_diversity/create/adsc/")


@tag("Adsc")
class TestAdscDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AdscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_adsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.AdscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "anidc_id",
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_adsc", f"/en/bio_diversity/details/adsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Adsc")
class TestAdscListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_adsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.AdscList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_adsc", f"/en/bio_diversity/list/adsc/")


@tag("Adsc")
class AdscUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.AdscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_adsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.AdscUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.AdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_adsc", f"/en/bio_diversity/update/adsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cnt")
class TestCntCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cnt')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cnt", "/en/bio_diversity/create/cnt/")


@tag("Cnt")
class TestCntDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cnt', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "loc_id",
            "cntc_id",
            "spec_id",
            "cnt",
            "est",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cnt", f"/en/bio_diversity/details/cnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cnt")
class TestCntListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cnt')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cnt", f"/en/bio_diversity/list/cnt/")


@tag("Cnt")
class CntUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cnt', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cnt", f"/en/bio_diversity/update/cnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntc")
class TestCntcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cntc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cntc", "/en/bio_diversity/create/cntc/")


@tag("Cntc")
class TestCntcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cntc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cntc", f"/en/bio_diversity/details/cntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntc")
class TestCntcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cntc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cntc", f"/en/bio_diversity/list/cntc/")


@tag("Cntc")
class CntcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cntc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cntc", f"/en/bio_diversity/update/cntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntd")
class TestCntdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cntd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cntd", "/en/bio_diversity/create/cntd/")


@tag("Cntd")
class TestCntdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cntd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CntdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "cnt_id",
            "anidc_id",
            "det_val",
            "adsc_id",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cntd", f"/en/bio_diversity/details/cntd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cntd")
class TestCntdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cntd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cntd", f"/en/bio_diversity/list/cntd/")


@tag("Cntd")
class CntdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CntdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cntd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CntdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cntd", f"/en/bio_diversity/update/cntd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Coll")
class TestCollCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CollFactory()
        self.test_url = reverse_lazy('bio_diversity:create_coll')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CollCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CollFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_coll", "/en/bio_diversity/create/coll/")


@tag("Coll")
class TestCollDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CollFactory()
        self.test_url = reverse_lazy('bio_diversity:details_coll', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CollDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_coll", f"/en/bio_diversity/details/coll/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Coll")
class TestCollListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_coll')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CollList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_coll", f"/en/bio_diversity/list/coll/")


@tag("Coll")
class CollUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CollFactory()
        self.test_url = reverse_lazy('bio_diversity:update_coll', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CollUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CollFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_coll", f"/en/bio_diversity/update/coll/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contdc")
class TestContdcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContdcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_contdc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContdcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_contdc", "/en/bio_diversity/create/contdc/")


@tag("Contdc")
class TestContdcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContdcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_contdc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContdcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "min_val",
            "max_val",
            "unit_id",
            "cont_subj_flag",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_contdc", f"/en/bio_diversity/details/contdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contdc")
class TestContdcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_contdc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContdcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_contdc", f"/en/bio_diversity/list/contdc/")


@tag("Contdc")
class ContdcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContdcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_contdc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContdcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_contdc", f"/en/bio_diversity/update/contdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contx")
class TestContxCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContxFactory()
        self.test_url = reverse_lazy('bio_diversity:create_contx')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContxCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContxFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_contx", "/en/bio_diversity/create/contx/")


@tag("Contx")
class TestContxDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContxFactory()
        self.test_url = reverse_lazy('bio_diversity:details_contx', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContxDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "evnt_id",
            "tank_id",
            "trof_id",
            "tray_id",
            "heat_id",
            "draw_id",
            "cup_id",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_contx", f"/en/bio_diversity/details/contx/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Contx")
class TestContxListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_contx')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContxList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_contx", f"/en/bio_diversity/list/contx/")


@tag("Contx")
class ContxUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ContxFactory()
        self.test_url = reverse_lazy('bio_diversity:update_contx', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ContxUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ContxFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_contx", f"/en/bio_diversity/update/contx/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cdsc")
class TestCdscCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CdscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cdsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CdscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cdsc", "/en/bio_diversity/create/cdsc/")


@tag("Cdsc")
class TestCdscDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CdscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cdsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CdscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "contdc_id",
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cdsc", f"/en/bio_diversity/details/cdsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cdsc")
class TestCdscListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cdsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CdscList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cdsc", f"/en/bio_diversity/list/cdsc/")


@tag("Cdsc")
class CdscUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CdscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cdsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CdscUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cdsc", f"/en/bio_diversity/update/cdsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cup")
class TestCupCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cup')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cup", "/en/bio_diversity/create/cup/")


@tag("Cup")
class TestCupDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cup', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cup", f"/en/bio_diversity/details/cup/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cup")
class TestCupListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cup')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cup", f"/en/bio_diversity/list/cup/")


@tag("Cup")
class CupUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cup', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cup", f"/en/bio_diversity/update/cup/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cupd")
class TestCupdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_cupd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_cupd", "/en/bio_diversity/create/cupd/")


@tag("Cupd")
class TestCupdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_cupd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "cup_id",
            "contdc_id",
            "det_value",
            "cdsc_id",
            "start_date",
            "end_date",
            "det_valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_cupd", f"/en/bio_diversity/details/cupd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Cupd")
class TestCupdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_cupd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupdList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_cupd", f"/en/bio_diversity/list/cupd/")


@tag("Cupd")
class CupdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.CupdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_cupd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.CupdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.CupdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_cupd", f"/en/bio_diversity/update/cupd/{self.instance.pk}/",
                                [self.instance.pk])



@tag("Data")
class TestDataCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:create_data')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.DataCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_data", "/en/bio_diversity/create/data/")


@tag("Data")
class TestDataCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:create_data')
        self.expected_template = 'shared_models/data_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.DrawCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_data", "/en/bio_diversity/create/data/")


@tag("Draw")
class TestDrawCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.DrawFactory()
        self.test_url = reverse_lazy('bio_diversity:create_draw')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.DrawCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.DrawFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_draw", "/en/bio_diversity/create/draw/")


@tag("Draw")
class TestDrawDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.DrawFactory()
        self.test_url = reverse_lazy('bio_diversity:details_draw', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.DrawDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_draw", f"/en/bio_diversity/details/draw/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Draw")
class TestDrawListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_draw')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.DrawList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_draw", f"/en/bio_diversity/list/draw/")


@tag("Draw")
class DrawUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.DrawFactory()
        self.test_url = reverse_lazy('bio_diversity:update_draw', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.DrawUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.DrawFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_draw", f"/en/bio_diversity/update/draw/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Env")
class TestEnvCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvFactory()
        self.test_url = reverse_lazy('bio_diversity:create_env')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_env", "/en/bio_diversity/create/env/")


@tag("Env")
class TestEnvDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvFactory()
        self.test_url = reverse_lazy('bio_diversity:details_env', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "loc_id",
            "inst_id",
            "envc_id",
            "env_val",
            "env_avg",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_env", f"/en/bio_diversity/details/env/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Env")
class TestEnvListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_env')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_env", f"/en/bio_diversity/list/env/")


@tag("Env")
class EnvUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvFactory()
        self.test_url = reverse_lazy('bio_diversity:update_env', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_env", f"/en/bio_diversity/update/env/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envc")
class TestEnvcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_envc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_envc", "/en/bio_diversity/create/envc/")


@tag("Envc")
class TestEnvcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_envc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "min_val",
            "max_val",
            "unit_id",
            "env_subj_flag",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_envc", f"/en/bio_diversity/details/envc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envc")
class TestEnvcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_envc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_envc", f"/en/bio_diversity/list/envc/")


@tag("Envc")
class EnvcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_envc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_envc", f"/en/bio_diversity/update/envc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envcf")
class TestEnvcfCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcfFactory()
        self.test_url = reverse_lazy('bio_diversity:create_envcf')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcfCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvcfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_envcf", "/en/bio_diversity/create/envcf/")


@tag("Envcf")
class TestEnvcfDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcfFactory()
        self.test_url = reverse_lazy('bio_diversity:details_envcf', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcfDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "env_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_envcf", f"/en/bio_diversity/details/envcf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envcf")
class TestEnvcfListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_envcf')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcfList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_envcf", f"/en/bio_diversity/list/envcf/")


@tag("Envcf")
class EnvcfUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvcfFactory()
        self.test_url = reverse_lazy('bio_diversity:update_envcf', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvcfUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvcfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_envcf", f"/en/bio_diversity/update/envcf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envsc")
class TestEnvscCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_envsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_envsc", "/en/bio_diversity/create/envsc/")


@tag("Envsc")
class TestEnvscDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_envsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            'envc_id',
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_envsc", f"/en/bio_diversity/details/envsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envsc")
class TestEnvscListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_envsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvscList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_envsc", f"/en/bio_diversity/list/envsc/")


@tag("Envsc")
class EnvscUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_envsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvscUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_envsc", f"/en/bio_diversity/update/envsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envt")
class TestEnvtCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvtFactory()
        self.test_url = reverse_lazy('bio_diversity:create_envt')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_envt", "/en/bio_diversity/create/envt/")


@tag("Envt")
class TestEnvtDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvtFactory()
        self.test_url = reverse_lazy('bio_diversity:details_envt', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "envtc_id",
            "lot_num",
            "amt",
            "unit_id",
            "duration",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_envt", f"/en/bio_diversity/details/envt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envt")
class TestEnvtListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_envt')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_envt", f"/en/bio_diversity/list/envt/")


@tag("Envt")
class EnvtUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvtFactory()
        self.test_url = reverse_lazy('bio_diversity:update_envt', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_envt", f"/en/bio_diversity/update/envt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envtc")
class TestEnvtcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvtcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_envtc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_envtc", "/en/bio_diversity/create/envtc/")


@tag("Envtc")
class TestEnvtcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvtcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_envtc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "rec_dose",
            "manufacturer",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_envtc", f"/en/bio_diversity/details/envtc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Envtc")
class TestEnvtcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_envtc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_envtc", f"/en/bio_diversity/list/envtc/")


@tag("Envtc")
class EnvtcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EnvtcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_envtc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EnvtcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EnvtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_envtc", f"/en/bio_diversity/update/envtc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evnt")
class TestEvntCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntFactory()
        self.test_url = reverse_lazy('bio_diversity:create_evnt')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_evnt", "/en/bio_diversity/create/evnt/")


@tag("Evnt")
class TestEvntDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntFactory()
        self.test_url = reverse_lazy('bio_diversity:details_evnt', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "facic_id",
            "evntc_id",
            "perc_id",
            "prog_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_evnt", f"/en/bio_diversity/details/evnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evnt")
class TestEvntListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_evnt')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_evnt", f"/en/bio_diversity/list/evnt/")


@tag("Evnt")
class EvntUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntFactory()
        self.test_url = reverse_lazy('bio_diversity:update_evnt', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_evnt", f"/en/bio_diversity/update/evnt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntc")
class TestEvntcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_evntc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_evntc", "/en/bio_diversity/create/evntc/")


@tag("Evntc")
class TestEvntcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_evntc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_evntc", f"/en/bio_diversity/details/evntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntc")
class TestEvntcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_evntc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_evntc", f"/en/bio_diversity/list/evntc/")


@tag("Evntc")
class EvntcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_evntc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_evntc", f"/en/bio_diversity/update/evntc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntf")
class TestEvntfCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntfFactory()
        self.test_url = reverse_lazy('bio_diversity:create_evntf')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_evntf", "/en/bio_diversity/create/evntf/")


@tag("Evntf")
class TestEvntfDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntfFactory()
        self.test_url = reverse_lazy('bio_diversity:details_evntf', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "evnt_id",
            "evntfc_id",
            "stok_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_evntf", f"/en/bio_diversity/details/evntf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntf")
class TestEvntfListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_evntf')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_evntf", f"/en/bio_diversity/list/evntf/")


@tag("Evntf")
class EvntfUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntfFactory()
        self.test_url = reverse_lazy('bio_diversity:update_evntf', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_evntf", f"/en/bio_diversity/update/evntf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntfc")
class TestEvntfcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntfcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_evntfc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntfcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_evntfc", "/en/bio_diversity/create/evntfc/")


@tag("Evntfc")
class TestEvntfcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntfcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_evntfc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_evntfc", f"/en/bio_diversity/details/evntfc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Evntfc")
class TestEvntfcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_evntfc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_evntfc", f"/en/bio_diversity/list/evntfc/")


@tag("Evntfc")
class EvntfcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.EvntfcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_evntfc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.EvntfcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.EvntfcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_evntfc", f"/en/bio_diversity/update/evntfc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Facic")
class TestFacicCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FacicFactory()
        self.test_url = reverse_lazy('bio_diversity:create_facic')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FacicCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FacicFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_facic", "/en/bio_diversity/create/facic/")


@tag("Facic")
class TestFacicDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FacicFactory()
        self.test_url = reverse_lazy('bio_diversity:details_facic', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FacicDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_facic", f"/en/bio_diversity/details/facic/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Facic")
class TestFacicListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_facic')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FacicList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_facic", f"/en/bio_diversity/list/facic/")


@tag("Facic")
class FacicUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FacicFactory()
        self.test_url = reverse_lazy('bio_diversity:update_facic', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FacicUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FacicFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_facic", f"/en/bio_diversity/update/facic/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Fecu")
class TestFecuCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FecuFactory()
        self.test_url = reverse_lazy('bio_diversity:create_fecu')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FecuCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FecuFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_fecu", "/en/bio_diversity/create/fecu/")


@tag("Fecu")
class TestFecuDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FecuFactory()
        self.test_url = reverse_lazy('bio_diversity:details_fecu', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FecuDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "stok_id",
            "coll_id",
            "start_date",
            "end_date",
            "alpha",
            "beta",
            "valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_fecu", f"/en/bio_diversity/details/fecu/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Fecu")
class TestFecuListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_fecu')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FecuList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_fecu", f"/en/bio_diversity/list/fecu/")


@tag("Fecu")
class FecuUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FecuFactory()
        self.test_url = reverse_lazy('bio_diversity:update_fecu', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FecuUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FecuFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_fecu", f"/en/bio_diversity/update/fecu/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feed")
class TestFeedCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedFactory()
        self.test_url = reverse_lazy('bio_diversity:create_feed')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_feed", "/en/bio_diversity/create/feed/")


@tag("Feed")
class TestFeedDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedFactory()
        self.test_url = reverse_lazy('bio_diversity:details_feed', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "feedm_id",
            "feedc_id",
            "lot_num",
            "amt",
            "unit_id",
            "freq",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_feed", f"/en/bio_diversity/details/feed/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feed")
class TestFeedListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_feed')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_feed", f"/en/bio_diversity/list/feed/")


@tag("Feed")
class FeedUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedFactory()
        self.test_url = reverse_lazy('bio_diversity:update_feed', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_feed", f"/en/bio_diversity/update/feed/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedc")
class TestFeedcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_feedc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_feedc", "/en/bio_diversity/create/feedc/")


@tag("Feedc")
class TestFeedcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_feedc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "manufacturer",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_feedc", f"/en/bio_diversity/details/feedc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedc")
class TestFeedcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_feedc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_feedc", f"/en/bio_diversity/list/feedc/")


@tag("Feedc")
class FeedcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_feedc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_feedc", f"/en/bio_diversity/update/feedc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedm")
class TestFeedmCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedmFactory()
        self.test_url = reverse_lazy('bio_diversity:create_feedm')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedmCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedmFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_feedm", "/en/bio_diversity/create/feedm/")


@tag("Feedm")
class TestFeedmDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedmFactory()
        self.test_url = reverse_lazy('bio_diversity:details_feedm', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedmDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_feedm", f"/en/bio_diversity/details/feedm/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Feedm")
class TestFeedmListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_feedm')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedmList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_feedm", f"/en/bio_diversity/list/feedm/")


@tag("Feedm")
class FeedmUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.FeedmFactory()
        self.test_url = reverse_lazy('bio_diversity:update_feedm', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.FeedmUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.FeedmFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_feedm", f"/en/bio_diversity/update/feedm/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Grp")
class TestGrpCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.GrpFactory()
        self.test_url = reverse_lazy('bio_diversity:create_grp')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.GrpFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_grp", "/en/bio_diversity/create/grp/")


@tag("Grp")
class TestGrpDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.GrpFactory()
        self.test_url = reverse_lazy('bio_diversity:details_grp', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "spec_id",
            "stok_id",
            "coll_id",
            "grp_valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_grp", f"/en/bio_diversity/details/grp/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Grp")
class TestGrpListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_grp')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_grp", f"/en/bio_diversity/list/grp/")


@tag("Grp")
class GrpUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.GrpFactory()
        self.test_url = reverse_lazy('bio_diversity:update_grp', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.GrpFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_grp", f"/en/bio_diversity/update/grp/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Grpd")
class TestGrpdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.GrpdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_grpd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.GrpdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_grpd", "/en/bio_diversity/create/grpd/")


@tag("Grpd")
class TestGrpdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.GrpdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_grpd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "anidc_id",
            "det_val",
            "adsc_id",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_grpd", f"/en/bio_diversity/details/grpd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Grpd")
class TestGrpdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_grpd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpdList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_grpd", f"/en/bio_diversity/list/grpd/")


@tag("Grpd")
class GrpdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.GrpdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_grpd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.GrpdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.GrpdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_grpd", f"/en/bio_diversity/update/grpd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heat")
class TestHeatCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatFactory()
        self.test_url = reverse_lazy('bio_diversity:create_heat')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_heat", "/en/bio_diversity/create/heat/")


@tag("Heat")
class TestHeatDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatFactory()
        self.test_url = reverse_lazy('bio_diversity:details_heat', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_heat", f"/en/bio_diversity/details/heat/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heat")
class TestHeatListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_heat')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_heat", f"/en/bio_diversity/list/heat/")


@tag("Heat")
class HeatUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatFactory()
        self.test_url = reverse_lazy('bio_diversity:update_heat', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_heat", f"/en/bio_diversity/update/heat/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heatd")
class TestHeatdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_heatd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_heatd", "/en/bio_diversity/create/heatd/")


@tag("Heatd")
class TestHeatdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_heatd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "heat_id",
            "contdc_id",
            "det_value",
            "cdsc_id",
            "start_date",
            "end_date",
            "det_valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_heatd", f"/en/bio_diversity/details/heatd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Heatd")
class TestHeatdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_heatd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatdList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_heatd", f"/en/bio_diversity/list/heatd/")


@tag("Heatd")
class HeatdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.HeatdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_heatd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.HeatdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.HeatdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_heatd", f"/en/bio_diversity/update/heatd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Img")
class TestImgCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ImgFactory()
        self.test_url = reverse_lazy('bio_diversity:create_img')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ImgFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_img", "/en/bio_diversity/create/img/")


@tag("Img")
class TestImgDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ImgFactory()
        self.test_url = reverse_lazy('bio_diversity:details_img', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "imgc_id",
            "tankd_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_img", f"/en/bio_diversity/details/img/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Img")
class TestImgListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_img')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_img", f"/en/bio_diversity/list/img/")


@tag("Img")
class ImgUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ImgFactory()
        self.test_url = reverse_lazy('bio_diversity:update_img', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ImgFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_img", f"/en/bio_diversity/update/img/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Imgc")
class TestImgcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ImgcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_imgc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ImgcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_imgc", "/en/bio_diversity/create/imgc/")


@tag("Imgc")
class TestImgcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ImgcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_imgc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_imgc", f"/en/bio_diversity/details/imgc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Imgc")
class TestImgcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_imgc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_imgc", f"/en/bio_diversity/list/imgc/")


@tag("Imgc")
class ImgcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ImgcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_imgc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ImgcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ImgcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_imgc", f"/en/bio_diversity/update/imgc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indv")
class TestIndvCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvFactory()
        self.test_url = reverse_lazy('bio_diversity:create_indv')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_indv", "/en/bio_diversity/create/indv/")


@tag("Indv")
class TestIndvDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvFactory()
        self.test_url = reverse_lazy('bio_diversity:details_indv', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "grp_id",
            "spec_id",
            "stok_id",
            "coll_id",
            "pit_tag",
            "indv_valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_indv", f"/en/bio_diversity/details/indv/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indv")
class TestIndvListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_indv')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_indv", f"/en/bio_diversity/list/indv/")


@tag("Indv")
class IndvUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvFactory()
        self.test_url = reverse_lazy('bio_diversity:update_indv', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_indv", f"/en/bio_diversity/update/indv/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indvd")
class TestIndvdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_indvd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_indvd", "/en/bio_diversity/create/indvd/")


@tag("Indvd")
class TestIndvdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_indvd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "anidc_id",
            "det_val",
            "adsc_id",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_indvd", f"/en/bio_diversity/details/indvd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indvd")
class TestIndvdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_indvd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvdList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_indvd", f"/en/bio_diversity/list/indvd/")


@tag("Indvd")
class IndvdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_indvd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_indvd", f"/en/bio_diversity/update/indvd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indvt")
class TestIndvtCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvtFactory()
        self.test_url = reverse_lazy('bio_diversity:create_indvt')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_indvt", "/en/bio_diversity/create/indvt/")


@tag("Indvt")
class TestIndvtDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvtFactory()
        self.test_url = reverse_lazy('bio_diversity:details_indvt', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "indvtc_id",
            "lot_num",
            "dose",
            "unit_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_indvt", f"/en/bio_diversity/details/indvt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indvt")
class TestIndvtListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_indvt')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_indvt", f"/en/bio_diversity/list/indvt/")


@tag("Indvt")
class IndvtUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvtFactory()
        self.test_url = reverse_lazy('bio_diversity:update_indvt', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_indvt", f"/en/bio_diversity/update/indvt/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indvtc")
class TestIndvtcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvtcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_indvtc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_indvtc", "/en/bio_diversity/create/indvtc/")


@tag("Indvtc")
class TestIndvtcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvtcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_indvtc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "rec_dose",
            "manufacturer",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_indvtc", f"/en/bio_diversity/details/indvtc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Indvtc")
class TestIndvtcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_indvtc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_indvtc", f"/en/bio_diversity/list/indvtc/")


@tag("Indvtc")
class IndvtcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.IndvtcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_indvtc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.IndvtcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.IndvtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_indvtc", f"/en/bio_diversity/update/indvtc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Inst")
class TestInstCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstFactory()
        self.test_url = reverse_lazy('bio_diversity:create_inst')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_inst", "/en/bio_diversity/create/inst/")


@tag("Inst")
class TestInstDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstFactory()
        self.test_url = reverse_lazy('bio_diversity:details_inst', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "instc_id",
            "serial_number",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_inst", f"/en/bio_diversity/details/inst/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Inst")
class TestInstListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_inst')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_inst", f"/en/bio_diversity/list/inst/")


@tag("Inst")
class InstUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstFactory()
        self.test_url = reverse_lazy('bio_diversity:update_inst', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_inst", f"/en/bio_diversity/update/inst/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instc")
class TestInstcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_instc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_instc", "/en/bio_diversity/create/instc/")


@tag("Instc")
class TestInstcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_instc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_instc", f"/en/bio_diversity/details/instc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instc")
class TestInstcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_instc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_instc", f"/en/bio_diversity/list/instc/")


@tag("Instc")
class InstcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_instc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_instc", f"/en/bio_diversity/update/instc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instd")
class TestInstdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_instd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_instd", "/en/bio_diversity/create/instd/")


@tag("Instd")
class TestInstdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_instd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "inst_id",
            "instdc_id",
            "det_value",
            "start_date",
            "end_date",
            "valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_instd", f"/en/bio_diversity/details/instd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instd")
class TestInstdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_instd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_instd", f"/en/bio_diversity/list/instd/")


@tag("Instd")
class InstdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_instd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_instd", f"/en/bio_diversity/update/instd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instdc")
class TestInstdcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_instdc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_instdc", "/en/bio_diversity/create/instdc/")


@tag("Instdc")
class TestInstdcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_instdc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstdcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_instdc", f"/en/bio_diversity/details/instdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Instdc")
class TestInstdcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_instdc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_instdc", f"/en/bio_diversity/list/instdc/")


@tag("Instdc")
class InstdcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.InstdcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_instdc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.InstdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_instdc", f"/en/bio_diversity/update/instdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Loc")
class TestLocCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocFactory()
        self.test_url = reverse_lazy('bio_diversity:create_loc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.LocCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_loc", "/en/bio_diversity/create/loc/")


@tag("Loc")
class TestLocDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocFactory()
        self.test_url = reverse_lazy('bio_diversity:details_loc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.LocDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "evnt_id",
            "locc_id",
            "rive_id",
            "trib_id",
            "subr_id",
            "relc_id",
            "loc_lat",
            "loc_lon",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_loc", f"/en/bio_diversity/details/loc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Loc")
class TestLocListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_loc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_loc", f"/en/bio_diversity/list/loc/")


@tag("Loc")
class LocUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocFactory()
        self.test_url = reverse_lazy('bio_diversity:update_loc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_loc", f"/en/bio_diversity/update/loc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locc")
class TestLoccCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LoccFactory()
        self.test_url = reverse_lazy('bio_diversity:create_locc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.LoccCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LoccFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_locc", "/en/bio_diversity/create/locc/")


@tag("Locc")
class TestLoccDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LoccFactory()
        self.test_url = reverse_lazy('bio_diversity:details_locc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.LoccDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_locc", f"/en/bio_diversity/details/locc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locc")
class TestLoccListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_locc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_locc", f"/en/bio_diversity/list/locc/")


@tag("Locc")
class LoccUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LoccFactory()
        self.test_url = reverse_lazy('bio_diversity:update_locc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LoccFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_locc", f"/en/bio_diversity/update/locc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locd")
class TestLocdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_locd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.LocdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_locd", "/en/bio_diversity/create/locd/")


@tag("Locd")
class TestLocdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_locd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.LocdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "locdc_id",
            "loc_id",
            "det_val",
            "ldsc_id",
            "qual_id",
            "detail_date",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_locd", f"/en/bio_diversity/details/locd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locd")
class TestLocdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_locd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_locd", f"/en/bio_diversity/list/locd/")


@tag("Locd")
class LocdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_locd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_locd", f"/en/bio_diversity/update/locd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locdc")
class TestLocdcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocdcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_locdc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.LocdcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_locdc", "/en/bio_diversity/create/locdc/")


@tag("Locdc")
class TestLocdcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocdcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_locdc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.LocdcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "min_val",
            "max_val",
            "unit_id",
            "loc_subj_flag",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_locdc", f"/en/bio_diversity/details/locdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Locdc")
class TestLocdcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_locdc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_locdc", f"/en/bio_diversity/list/locdc/")


@tag("Locdc")
class LocdcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LocdcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_locdc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LocdcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_locdc", f"/en/bio_diversity/update/locdc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Ldsc")
class TestLdscCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LdscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_ldsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.LdscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_ldsc", "/en/bio_diversity/create/ldsc/")


@tag("Ldsc")
class TestLdscDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LdscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_ldsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.LdscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_ldsc", f"/en/bio_diversity/details/ldsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Ldsc")
class TestLdscListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_ldsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_ldsc", f"/en/bio_diversity/list/ldsc/")


@tag("Ldsc")
class LdscUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.LdscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_ldsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.LdscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_ldsc", f"/en/bio_diversity/update/ldsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Move")
class TestMoveCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.MoveFactory()
        self.test_url = reverse_lazy('bio_diversity:create_move')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.MoveCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.MoveFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_move", "/en/bio_diversity/create/move/")


@tag("Move")
class TestMoveDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.MoveFactory()
        self.test_url = reverse_lazy('bio_diversity:details_move', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.MoveDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "move_date",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_move", f"/en/bio_diversity/details/move/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Move")
class TestMoveListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_move')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_move", f"/en/bio_diversity/list/move/")


@tag("Move")
class MoveUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.MoveFactory()
        self.test_url = reverse_lazy('bio_diversity:update_move', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.MoveFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_move", f"/en/bio_diversity/update/move/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Orga")
class TestOrgaCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.OrgaFactory()
        self.test_url = reverse_lazy('bio_diversity:create_orga')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.OrgaCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.OrgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_orga", "/en/bio_diversity/create/orga/")


@tag("Orga")
class TestOrgaDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.OrgaFactory()
        self.test_url = reverse_lazy('bio_diversity:details_orga', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.OrgaDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_orga", f"/en/bio_diversity/details/orga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Orga")
class TestOrgaListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_orga')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_orga", f"/en/bio_diversity/list/orga/")


@tag("Orga")
class OrgaUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.OrgaFactory()
        self.test_url = reverse_lazy('bio_diversity:update_orga', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.OrgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_orga", f"/en/bio_diversity/update/orga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Pair")
class TestPairCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PairFactory()
        self.test_url = reverse_lazy('bio_diversity:create_pair')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.PairCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PairFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_pair", "/en/bio_diversity/create/pair/")


@tag("Pair")
class TestPairDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PairFactory()
        self.test_url = reverse_lazy('bio_diversity:details_pair', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.PairDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "indv_id",
            "start_date",
            "end_date",
            "valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_pair", f"/en/bio_diversity/details/pair/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Pair")
class TestPairListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_pair')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_pair", f"/en/bio_diversity/list/pair/")


@tag("Pair")
class PairUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PairFactory()
        self.test_url = reverse_lazy('bio_diversity:update_pair', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PairFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_pair", f"/en/bio_diversity/update/pair/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Perc")
class TestPercCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PercFactory()
        self.test_url = reverse_lazy('bio_diversity:create_perc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.PercCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PercFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_perc", "/en/bio_diversity/create/perc/")


@tag("Perc")
class TestPercDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PercFactory()
        self.test_url = reverse_lazy('bio_diversity:details_perc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.PercDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "perc_first_name",
            "perc_last_name",
            "perc_valid",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_perc", f"/en/bio_diversity/details/perc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Perc")
class TestPercListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_perc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_perc", f"/en/bio_diversity/list/perc/")


@tag("Perc")
class PercUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PercFactory()
        self.test_url = reverse_lazy('bio_diversity:update_perc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PercFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_perc", f"/en/bio_diversity/update/perc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prio")
class TestPrioCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PrioFactory()
        self.test_url = reverse_lazy('bio_diversity:create_prio')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.PrioCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PrioFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_prio", "/en/bio_diversity/create/prio/")


@tag("Prio")
class TestPrioDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PrioFactory()
        self.test_url = reverse_lazy('bio_diversity:details_prio', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.PrioDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_prio", f"/en/bio_diversity/details/prio/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prio")
class TestPrioListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_prio')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.PrioList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_prio", f"/en/bio_diversity/list/prio/")


@tag("Prio")
class PrioUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.PrioFactory()
        self.test_url = reverse_lazy('bio_diversity:update_prio', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.PrioUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.PrioFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_prio", f"/en/bio_diversity/update/prio/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prog")
class TestProgCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgFactory()
        self.test_url = reverse_lazy('bio_diversity:create_prog')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProgCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_prog", "/en/bio_diversity/create/prog/")


@tag("Prog")
class TestProgDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgFactory()
        self.test_url = reverse_lazy('bio_diversity:details_prog', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProgDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "prog_name",
            "prog_desc",
            "proga_id",
            "orga_id",
            "start_date",
            "end_date",
            "valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_prog", f"/en/bio_diversity/details/prog/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prog")
class TestProgListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_prog')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_prog", f"/en/bio_diversity/list/prog/")


@tag("Prog")
class ProgUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgFactory()
        self.test_url = reverse_lazy('bio_diversity:update_prog', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_prog", f"/en/bio_diversity/update/prog/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Proga")
class TestProgaCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgaFactory()
        self.test_url = reverse_lazy('bio_diversity:create_proga')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProgaCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_proga", "/en/bio_diversity/create/proga/")


@tag("Proga")
class TestProgaDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgaFactory()
        self.test_url = reverse_lazy('bio_diversity:details_proga', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProgaDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "proga_last_name",
            "proga_first_name",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_proga", f"/en/bio_diversity/details/proga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Proga")
class TestProgaListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_proga')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_proga", f"/en/bio_diversity/list/proga/")


@tag("Proga")
class ProgaUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProgaFactory()
        self.test_url = reverse_lazy('bio_diversity:update_proga', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProgaFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_proga", f"/en/bio_diversity/update/proga/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prot")
class TestProtCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtFactory()
        self.test_url = reverse_lazy('bio_diversity:create_prot')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_prot", "/en/bio_diversity/create/prot/")


@tag("Prot")
class TestProtDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtFactory()
        self.test_url = reverse_lazy('bio_diversity:details_prot', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "prog_id",
            "protc_id",
            "evntc_id",
            "prot_desc",
            "start_date",
            "end_date",
            "valid",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_prot", f"/en/bio_diversity/details/prot/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Prot")
class TestProtListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_prot')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_prot", f"/en/bio_diversity/list/prot/")


@tag("Prot")
class ProtUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtFactory()
        self.test_url = reverse_lazy('bio_diversity:update_prot', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_prot", f"/en/bio_diversity/update/prot/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protc")
class TestProtcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_protc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_protc", "/en/bio_diversity/create/protc/")


@tag("Protc")
class TestProtcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_protc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_protc", f"/en/bio_diversity/details/protc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protc")
class TestProtcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_protc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_protc", f"/en/bio_diversity/list/protc/")


@tag("Protc")
class ProtcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_protc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_protc", f"/en/bio_diversity/update/protc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protf")
class TestProtfCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtfFactory()
        self.test_url = reverse_lazy('bio_diversity:create_protf')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtfCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_protf", "/en/bio_diversity/create/protf/")


@tag("Protf")
class TestProtfDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtfFactory()
        self.test_url = reverse_lazy('bio_diversity:details_protf', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.ProtfDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "prot_id",
            "protf_pdf",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_protf", f"/en/bio_diversity/details/protf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Protf")
class TestProtfListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_protf')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_protf", f"/en/bio_diversity/list/protf/")


@tag("Protf")
class ProtfUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.ProtfFactory()
        self.test_url = reverse_lazy('bio_diversity:update_protf', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.ProtfFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_protf", f"/en/bio_diversity/update/protf/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Qual")
class TestQualCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.QualFactory()
        self.test_url = reverse_lazy('bio_diversity:create_qual')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.QualCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.QualFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_qual", "/en/bio_diversity/create/qual/")


@tag("Qual")
class TestQualDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.QualFactory()
        self.test_url = reverse_lazy('bio_diversity:details_qual', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.QualDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_qual", f"/en/bio_diversity/details/qual/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Qual")
class TestQualListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_qual')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.QualList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_qual", f"/en/bio_diversity/list/qual/")


@tag("Qual")
class QualUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.QualFactory()
        self.test_url = reverse_lazy('bio_diversity:update_qual', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.QualUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.QualFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_qual", f"/en/bio_diversity/update/qual/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Relc")
class TestRelcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RelcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_relc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.RelcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RelcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_relc", "/en/bio_diversity/create/relc/")


@tag("Relc")
class TestRelcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RelcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_relc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.RelcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_relc", f"/en/bio_diversity/details/relc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Relc")
class TestRelcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_relc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_relc", f"/en/bio_diversity/list/relc/")


@tag("Relc")
class RelcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RelcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_relc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RelcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_relc", f"/en/bio_diversity/update/relc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Rive")
class TestRiveCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RiveFactory()
        self.test_url = reverse_lazy('bio_diversity:create_rive')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.RiveCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RiveFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_rive", "/en/bio_diversity/create/rive/")


@tag("Rive")
class TestRiveDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RiveFactory()
        self.test_url = reverse_lazy('bio_diversity:details_rive', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.RiveDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_rive", f"/en/bio_diversity/details/rive/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Rive")
class TestRiveListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_rive')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_rive", f"/en/bio_diversity/list/rive/")


@tag("Rive")
class RiveUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RiveFactory()
        self.test_url = reverse_lazy('bio_diversity:update_rive', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RiveFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_rive", f"/en/bio_diversity/update/rive/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Role")
class TestRoleCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RoleFactory()
        self.test_url = reverse_lazy('bio_diversity:create_role')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.RoleCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RoleFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_role", "/en/bio_diversity/create/role/")


@tag("Role")
class TestRoleDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RoleFactory()
        self.test_url = reverse_lazy('bio_diversity:details_role', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.RoleDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_role", f"/en/bio_diversity/details/role/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Role")
class TestRoleListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_role')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_role", f"/en/bio_diversity/list/role/")


@tag("Role")
class RoleUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.RoleFactory()
        self.test_url = reverse_lazy('bio_diversity:update_role', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.RoleFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_role", f"/en/bio_diversity/update/role/{self.instance.pk}/",
                                [self.instance.pk])


@tag("amp")
class TestSampCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampFactory()
        self.test_url = reverse_lazy('bio_diversity:create_samp')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_samp", "/en/bio_diversity/create/samp/")


@tag("Samp")
class TestSampDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampFactory()
        self.test_url = reverse_lazy('bio_diversity:details_samp', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "loc_id",
            "samp_num",
            "spec_id",
            "sampc_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_samp", f"/en/bio_diversity/details/samp/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Samp")
class TestSampListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_samp')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_samp", f"/en/bio_diversity/list/samp/")


@tag("Samp")
class SampUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampFactory()
        self.test_url = reverse_lazy('bio_diversity:update_samp', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_samp", f"/en/bio_diversity/update/samp/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampc")
class TestSampcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_sampc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_sampc", "/en/bio_diversity/create/sampc/")


@tag("Sampc")
class TestSampcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_sampc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_sampc", f"/en/bio_diversity/details/sampc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampc")
class TestSampcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_sampc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_sampc", f"/en/bio_diversity/list/sampc/")


@tag("Sampc")
class SampcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_sampc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_sampc", f"/en/bio_diversity/update/sampc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampd")
class TestSampdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_sampd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_sampd", "/en/bio_diversity/create/sampd/")


@tag("Sampd")
class TestSampdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_sampd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SampdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "samp_id",
            "anidc_id",
            "det_val",
            "adsc_id",
            "qual_id",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_sampd", f"/en/bio_diversity/details/sampd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sampd")
class TestSampdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_sampd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_sampd", f"/en/bio_diversity/list/sampd/")


@tag("Sampd")
class SampdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SampdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_sampd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SampdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_sampd", f"/en/bio_diversity/update/sampd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sire")
class TestSireCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SireFactory()
        self.test_url = reverse_lazy('bio_diversity:create_sire')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SireCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SireFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_sire", "/en/bio_diversity/create/sire/")


@tag("Sire")
class TestSireDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SireFactory()
        self.test_url = reverse_lazy('bio_diversity:details_sire', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SireDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "prio_id",
            "pair_id",
            "indv_id",
            "choice",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_sire", f"/en/bio_diversity/details/sire/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Sire")
class TestSireListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_sire')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_sire", f"/en/bio_diversity/list/sire/")


@tag("Sire")
class SireUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SireFactory()
        self.test_url = reverse_lazy('bio_diversity:update_sire', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SireFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_sire", f"/en/bio_diversity/update/sire/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spwnd")
class TestSpwndCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwndFactory()
        self.test_url = reverse_lazy('bio_diversity:create_spwnd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpwndFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_spwnd", "/en/bio_diversity/create/spwnd/")


@tag("Spwnd")
class TestSpwndDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwndFactory()
        self.test_url = reverse_lazy('bio_diversity:details_spwnd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "pair_id",
            "spwndc_id",
            "spwnsc_id",
            "qual_id",
            "det_val",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_spwnd",
                                f"/en/bio_diversity/details/spwnd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spwnd")
class TestSpwndListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_spwnd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_spwnd", f"/en/bio_diversity/list/spwnd/")


@tag("Spwnd")
class SpwndUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwndFactory()
        self.test_url = reverse_lazy('bio_diversity:update_spwnd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpwndFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_spwnd",
                                f"/en/bio_diversity/update/spwnd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spwndc")
class TestSpwndcCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwndcFactory()
        self.test_url = reverse_lazy('bio_diversity:create_spwndc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndcCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpwndcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_spwndc", "/en/bio_diversity/create/spwndc/")


@tag("Spwndc")
class TestSpwndcDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwndcFactory()
        self.test_url = reverse_lazy('bio_diversity:details_spwndc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndcDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "min_val",
            "max_val",
            "unit_id",
            "spwn_subj_flag",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_spwndc", f"/en/bio_diversity/details/spwndc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spwndc")
class TestSpwndcListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_spwndc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndcList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_spwndc", f"/en/bio_diversity/list/spwndc/")


@tag("Spwndc")
class SpwndcUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwndcFactory()
        self.test_url = reverse_lazy('bio_diversity:update_spwndc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwndcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpwndcFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_spwndc", f"/en/bio_diversity/update/spwndc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spwnsc")
class TestSpwnscCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwnscFactory()
        self.test_url = reverse_lazy('bio_diversity:create_spwnsc')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwnscCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpwnscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_spwnsc", "/en/bio_diversity/create/spwnsc/")


@tag("Spwnsc")
class TestSpwnscDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwnscFactory()
        self.test_url = reverse_lazy('bio_diversity:details_spwnsc', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwnscDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "spwndc_id",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_spwnsc", f"/en/bio_diversity/details/spwnsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spwnsc")
class TestSpwnscListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_spwnsc')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwnscList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_spwnsc", f"/en/bio_diversity/list/spwnsc/")


@tag("Spwnsc")
class SpwnscUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpwnscFactory()
        self.test_url = reverse_lazy('bio_diversity:update_spwnsc', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpwnscUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpwnscFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_spwnsc", f"/en/bio_diversity/update/spwnsc/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spec")
class TestSpecCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpecFactory()
        self.test_url = reverse_lazy('bio_diversity:create_spec')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpecCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpecFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_spec", "/en/bio_diversity/create/spec/")


@tag("Spec")
class TestSpecDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpecFactory()
        self.test_url = reverse_lazy('bio_diversity:details_spec', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SpecDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "species",
            "com_name",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_spec", f"/en/bio_diversity/details/spec/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Spec")
class TestSpecListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_spec')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_spec", f"/en/bio_diversity/list/spec/")


@tag("Spec")
class SpecUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SpecFactory()
        self.test_url = reverse_lazy('bio_diversity:update_spec', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SpecFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_spec", f"/en/bio_diversity/update/spec/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Stok")
class TestStokCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.StokFactory()
        self.test_url = reverse_lazy('bio_diversity:create_stok')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.StokCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.StokFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_stok", "/en/bio_diversity/create/stok/")


@tag("Stok")
class TestStokDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.StokFactory()
        self.test_url = reverse_lazy('bio_diversity:details_stok', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.StokDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_stok", f"/en/bio_diversity/details/stok/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Stok")
class TestStokListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_stok')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.StokList, GenericList)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_stok", f"/en/bio_diversity/list/stok/")


@tag("Stok")
class StokUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.StokFactory()
        self.test_url = reverse_lazy('bio_diversity:update_stok', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.StokUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.StokFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_stok", f"/en/bio_diversity/update/stok/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Subr")
class TestSubrCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SubrFactory()
        self.test_url = reverse_lazy('bio_diversity:create_subr')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.SubrCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SubrFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_subr", "/en/bio_diversity/create/subr/")


@tag("Subr")
class TestSubrDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SubrFactory()
        self.test_url = reverse_lazy('bio_diversity:details_subr', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.SubrDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "rive_id",
            "trib_id",
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_subr", f"/en/bio_diversity/details/subr/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Subr")
class TestSubrListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_subr')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_subr", f"/en/bio_diversity/list/subr/")


@tag("Subr")
class SubrUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.SubrFactory()
        self.test_url = reverse_lazy('bio_diversity:update_subr', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.SubrFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_subr", f"/en/bio_diversity/update/subr/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tank")
class TestTankCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankFactory()
        self.test_url = reverse_lazy('bio_diversity:create_tank')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TankCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_tank", "/en/bio_diversity/create/tank/")


@tag("Tank")
class TestTankDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankFactory()
        self.test_url = reverse_lazy('bio_diversity:details_tank', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TankDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_tank",
                                f"/en/bio_diversity/details/tank/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tank")
class TestTankListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_tank')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_tank", f"/en/bio_diversity/list/tank/")


@tag("Tank")
class TankUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankFactory()
        self.test_url = reverse_lazy('bio_diversity:update_tank', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_tank",
                                f"/en/bio_diversity/update/tank/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tankd")
class TestTankdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_tankd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TankdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_tankd", "/en/bio_diversity/create/tankd/")


@tag("Tankd")
class TestTankdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_tankd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TankdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "tank_id",
            "contdc_id",
            "det_value",
            "cdsc_id",
            "start_date",
            "end_date",
            "det_valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_tankd",
                                f"/en/bio_diversity/details/tankd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tankd")
class TestTankdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_tankd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_tankd", f"/en/bio_diversity/list/tankd/")


@tag("Tankd")
class TankdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TankdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_tankd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TankdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_tankd",
                                f"/en/bio_diversity/update/tankd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Team")
class TestTeamCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TeamFactory()
        self.test_url = reverse_lazy('bio_diversity:create_team')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TeamCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TeamFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_team", "/en/bio_diversity/create/team/")


@tag("Team")
class TestTeamDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TeamFactory()
        self.test_url = reverse_lazy('bio_diversity:details_team', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TeamDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "perc_id",
            "role_id",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_team", f"/en/bio_diversity/details/team/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Team")
class TestTeamListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_team')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_team", f"/en/bio_diversity/list/team/")


@tag("Team")
class TeamUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TeamFactory()
        self.test_url = reverse_lazy('bio_diversity:update_team', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TeamFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_team",
                                f"/en/bio_diversity/update/team/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tray")
class TestTrayCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrayFactory()
        self.test_url = reverse_lazy('bio_diversity:create_tray')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrayCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrayFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_tray", "/en/bio_diversity/create/tray/")


@tag("Tray")
class TestTrayDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrayFactory()
        self.test_url = reverse_lazy('bio_diversity:details_tray', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrayDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_tray", f"/en/bio_diversity/details/tray/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Tray")
class TestTrayListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_tray')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_tray", f"/en/bio_diversity/list/tray/")


@tag("Tray")
class TrayUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrayFactory()
        self.test_url = reverse_lazy('bio_diversity:update_tray', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrayFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_tray", f"/en/bio_diversity/update/tray/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trayd")
class TestTraydCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TraydFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trayd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TraydCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TraydFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trayd", "/en/bio_diversity/create/trayd/")


@tag("Trayd")
class TestTraydDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TraydFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trayd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TraydDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "tray_id",
            "contdc_id",
            "det_value",
            "cdsc_id",
            "start_date",
            "end_date",
            "det_valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trayd", f"/en/bio_diversity/details/trayd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trayd")
class TestTraydListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trayd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trayd", f"/en/bio_diversity/list/trayd/")


@tag("Trayd")
class TraydUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TraydFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trayd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TraydFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trayd", f"/en/bio_diversity/update/trayd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trib")
class TestTribCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TribFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trib')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TribCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TribFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trib", "/en/bio_diversity/create/trib/")


@tag("Trib")
class TestTribDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TribFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trib', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TribDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "rive_id",
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trib", f"/en/bio_diversity/details/trib/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trib")
class TestTribListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trib')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trib", f"/en/bio_diversity/list/trib/")


@tag("Trib")
class TribUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TribFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trib', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TribFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trib", f"/en/bio_diversity/update/trib/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trof")
class TestTrofCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trof')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrofCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trof", "/en/bio_diversity/create/trof/")


@tag("Trof")
class TestTrofDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trof', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrofDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trof", f"/en/bio_diversity/details/trof/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trof")
class TestTrofListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trof')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trof", f"/en/bio_diversity/list/trof/")


@tag("Trof")
class TrofUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trof', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trof", f"/en/bio_diversity/update/trof/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trofd")
class TestTrofdCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofdFactory()
        self.test_url = reverse_lazy('bio_diversity:create_trofd')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrofdCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_trofd", "/en/bio_diversity/create/trofd/")


@tag("Trofd")
class TestTrofdDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofdFactory()
        self.test_url = reverse_lazy('bio_diversity:details_trofd', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.TrofdDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "trof_id",
            "contdc_id",
            "det_value",
            "cdsc_id",
            "start_date",
            "end_date",
            "det_valid",
            "comments",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_trofd", f"/en/bio_diversity/details/trofd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Trofd")
class TestTrofdListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_trofd')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_trofd", f"/en/bio_diversity/list/trofd/")


@tag("Trofd")
class TrofdUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.TrofdFactory()
        self.test_url = reverse_lazy('bio_diversity:update_trofd', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.TrofdFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_trofd", f"/en/bio_diversity/update/trofd/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Unit")
class TestUnitCreateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.UnitFactory()
        self.test_url = reverse_lazy('bio_diversity:create_unit')
        self.expected_template = 'shared_models/shared_entry_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.UnitCreate, CommonCreate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.UnitFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:create_unit", "/en/bio_diversity/create/unit/")


@tag("Unit")
class TestUnitDetailView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.UnitFactory()
        self.test_url = reverse_lazy('bio_diversity:details_unit', args=[self.instance.pk, ])
        self.expected_template = 'bio_diversity/bio_details.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        self.assert_inheritance(views.UnitDetails, CommonDetails)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_context(self):
        context_vars = [
            "name",
            "nom",
            "description_en",
            "description_fr",
            "created_by",
            "created_date",
        ]
        self.assert_field_in_field_list(self.test_url, 'fields', context_vars, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:details_unit", f"/en/bio_diversity/details/unit/{self.instance.pk}/",
                                [self.instance.pk])


@tag("Unit")
class TestUnitListView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('bio_diversity:list_unit')
        self.expected_template = 'shared_models/shared_filter.html'
        self.user = self.login_bio_author_user()

    def test_view_class(self):
        # view
        self.assert_inheritance(views.InstcList, GenericList)

    def test_view(self):
        # access
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_correct_url(self):
        # correct url
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:list_unit", f"/en/bio_diversity/list/unit/")


@tag("Unit")
class UnitUpdateView(CommonBioTest):
    def setUp(self):
        super().setUp()
        self.instance = BioFactoryFloor.UnitFactory()
        self.test_url = reverse_lazy('bio_diversity:update_unit', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/shared_models_update_form.html'
        self.user = self.login_bio_admin_user()

    def test_view_class(self):
        self.assert_inheritance(views.InstcUpdate, CommonUpdate)

    def test_view(self):
        self.assert_good_response(self.test_url)
        # self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    def test_submit(self):
        data = BioFactoryFloor.UnitFactory.build_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("bio_diversity:update_unit", f"/en/bio_diversity/update/unit/{self.instance.pk}/",
                                [self.instance.pk])
