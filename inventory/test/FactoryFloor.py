import factory
from django.utils import timezone
from faker import Faker

from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory
from .. import models
from ..data_fixtures import resource_types, statuses

faker = Faker()


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Organization

    name_eng = factory.lazy_attribute(lambda o: faker.company())
    name_fre = factory.lazy_attribute(lambda o: faker.company())
    address = factory.lazy_attribute(lambda o: faker.address())
    city = factory.lazy_attribute(lambda o: faker.city())


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Person
        django_get_or_create = ('user',)  # needed because a Person is automatically created when a user is created (via signals)

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)


class KeywordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Keyword

    text_value_eng = factory.lazy_attribute(lambda o: faker.word())
    is_taxonomic = factory.lazy_attribute(lambda o: faker.pybool())
    keyword_domain = factory.lazy_attribute(
        lambda o: models.KeywordDomain.objects.all()[faker.random_int(0, models.KeywordDomain.objects.count() - 1)])


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Resource

    uuid = factory.lazy_attribute(lambda o: faker.uuid4())
    resource_type = factory.lazy_attribute(lambda o: resource_types.get_choices()[faker.random_int(0, len(resource_types.get_choices()) - 1)][0])
    section = factory.SubFactory(SectionFactory)
    title_eng = factory.lazy_attribute(lambda o: faker.catch_phrase())
    status = factory.lazy_attribute(lambda o: statuses.get_choices()[faker.random_int(0, len(statuses.get_choices()) - 1)][0])
    purpose_eng = factory.lazy_attribute(lambda o: faker.text())
    descr_eng = factory.lazy_attribute(lambda o: faker.text())
    time_start_day = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()).day)
    time_start_month = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()).month)
    time_start_year = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()).year)

    @staticmethod
    def get_valid_data():
        start_date = faker.future_datetime(tzinfo=timezone.get_current_timezone())
        return {
            "section": SectionFactory().id,
            "title_eng": faker.catch_phrase(),
            "descr_eng": faker.text(),
            "purpose_eng": faker.text(),
            "resource_type": resource_types.get_choices()[faker.random_int(0, len(resource_types.get_choices()) - 1)][0],
            "time_start_day": start_date.day,
            "time_start_month": start_date.month,
            "time_start_year": start_date.year,
            "had_sharing_agreements": 0,
        }


class DataResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DataResource

    resource = factory.SubFactory(ResourceFactory)
    url = factory.lazy_attribute(lambda o: faker.url())
    content_type = factory.lazy_attribute(
        lambda o: models.ContentType.objects.all()[faker.random_int(0, models.ContentType.objects.count() - 1)])
    name_eng = factory.lazy_attribute(lambda o: faker.catch_phrase())
    name_fre = factory.lazy_attribute(lambda o: faker.catch_phrase())
    protocol = factory.lazy_attribute(lambda o: faker.word())


class WebServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DataResource

    resource = factory.SubFactory(ResourceFactory)
    url = factory.lazy_attribute(lambda o: faker.url())
    content_type = factory.lazy_attribute(
        lambda o: models.ContentType.objects.all()[faker.random_int(0, models.ContentType.objects.count() - 1)])
    name_eng = factory.lazy_attribute(lambda o: faker.catch_phrase())
    name_fre = factory.lazy_attribute(lambda o: faker.catch_phrase())
    protocol = factory.lazy_attribute(lambda o: faker.word())
    service_language = factory.lazy_attribute(lambda o: faker.word())


class ResourcePersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ResourcePerson2

    resource = factory.SubFactory(ResourceFactory)
    user = factory.SubFactory(UserFactory)
    # role = factory.lazy_attribute(lambda o: models.PersonRole.objects.all()[faker.random_int(0, models.PersonRole.objects.count() - 1)])


class ResourceCertificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ResourceCertification

    resource = factory.SubFactory(ResourceFactory)
    certifying_user = factory.SubFactory(UserFactory)
    certification_date = factory.lazy_attribute(lambda o: faker.date_time_this_year(tzinfo=timezone.get_current_timezone()))
    notes = factory.lazy_attribute(lambda o: faker.catch_phrase())
