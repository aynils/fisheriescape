import csv
import datetime as dt
import random
from io import StringIO

import requests
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.timezone import utc, make_aware
from django.utils.translation import gettext_lazy, gettext as _

from lib.templatetags.custom_filters import nz
from shared_models.utils import get_labels
from shared_models.views import CommonTemplateView, CommonHardDeleteView, CommonFormsetView, CommonFormView, CommonDeleteView, CommonDetailView, \
    CommonCreateView, CommonUpdateView, CommonFilterView, CommonPopoutCreateView, CommonPopoutUpdateView, CommonPopoutDeleteView, CommonListView
from . import models, forms, filters, utils, reports
from .mixins import ednaBasicMixin, eDNAAdminRequiredMixin, SuperuserOrAdminRequiredMixin


class ednaUserFormsetView(SuperuserOrAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage eDNA Users"
    queryset = models.ednaUser.objects.all()
    formset_class = forms.ednaUserFormset
    success_url_name = "edna:manage_edna_users"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_edna_user"
    container_class = "container bg-light curvy"


class ednaUserHardDeleteView(SuperuserOrAdminRequiredMixin, CommonHardDeleteView):
    model = models.ednaUser
    success_url = reverse_lazy("edna:manage_edna_users")


class IndexTemplateView(ednaBasicMixin, CommonTemplateView):
    h1 = "home"
    active_page_name_crumb = "home"
    template_name = 'edna/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source = "GATC"
        random.seed()
        txt = ""
        for i in range(1, 9000):
            txt += random.sample("GATC", 1)[0]
        context["txt"] = txt
        return context


# REFERENCE TABLES #
####################

class FiltrationTypeFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage Fitlration Types"
    queryset = models.FiltrationType.objects.all()
    formset_class = forms.FiltrationTypeFormset
    success_url_name = "edna:manage_filtration_types"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_filtration_type"


class FiltrationTypeHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.FiltrationType
    success_url = reverse_lazy("edna:manage_filtration_types")


class DNAExtractionProtocolFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage DNA Extraction Protocols"
    queryset = models.DNAExtractionProtocol.objects.all()
    formset_class = forms.DNAExtractionProtocolFormset
    success_url_name = "edna:manage_dna_extraction_protocols"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_dna_extraction_protocol"


class DNAExtractionProtocolHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.DNAExtractionProtocol
    success_url = reverse_lazy("edna:manage_dna_extraction_protocols")


class TagFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage Tags"
    queryset = models.Tag.objects.all()
    formset_class = forms.TagFormset
    success_url_name = "edna:manage_tags"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_tag"


class TagHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.Tag
    success_url = reverse_lazy("edna:manage_tags")


class SampleTypeFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage Sample Types"
    queryset = models.SampleType.objects.all()
    formset_class = forms.SampleTypeFormset
    success_url_name = "edna:manage_sample_types"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_sample_type"


class SampleTypeHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.SampleType
    success_url = reverse_lazy("edna:manage_sample_types")


class MasterMixFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage Master Mixes"
    queryset = models.MasterMix.objects.all()
    formset_class = forms.MasterMixFormset
    success_url_name = "edna:manage_master_mixes"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_master_mix"


class MasterMixHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.MasterMix
    success_url = reverse_lazy("edna:manage_master_mixes")


# SPECIES #
###########

class SpeciesListView(eDNAAdminRequiredMixin, CommonFilterView):
    template_name = 'edna/list.html'
    filterset_class = filters.SpeciesFilter
    home_url_name = "edna:index"
    new_object_url = reverse_lazy("edna:species_new")
    row_object_url_name = row_ = "edna:species_detail"
    container_class = "container-fluid curvy"

    field_list = [
        {"name": 'tcommon|{}'.format("common name"), "class": "", "width": ""},
        {"name": 'formatted_scientific|{}'.format("scientific name"), "class": "", "width": ""},
    ]

    def get_queryset(self):
        return models.Species.objects.annotate(
            search_term=Concat('common_name_en', Value(" "), 'common_name_fr', Value(" "), 'scientific_name', output_field=TextField()))


class SpeciesUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("edna:species_list")}
    container_class = "container curvy"


class SpeciesCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.Species
    form_class = forms.SpeciesForm
    success_url = reverse_lazy('edna:species_list')
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("edna:species_list")}
    container_class = "container curvy"


class SpeciesDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Species
    template_name = 'edna/species_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("edna:species_list")}
    container_class = "container curvy"
    field_list = [
        'tcommon|{}'.format("common name"),
        'formatted_scientific|{}'.format("scientific name"),
        'tsn',
        'aphia_id',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpeciesDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.Species
    success_url = reverse_lazy('edna:species_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container curvy"


# ASSAY #
###########

class AssayListView(eDNAAdminRequiredMixin, CommonListView):
    template_name = 'edna/list.html'
    home_url_name = "edna:index"
    new_object_url = reverse_lazy("edna:assay_new")
    row_object_url_name = row_ = "edna:assay_detail"
    container_class = "container-fluid curvy"
    model = models.Assay

    field_list = [
        {"name": 'alias', "class": "", "width": ""},
        {"name": 'name', "class": "", "width": ""},
        {"name": 'lod', "class": "", "width": ""},
        {"name": 'loq', "class": "", "width": ""},
        {"name": 'units', "class": "", "width": ""},
        {"name": 'a_coef', "class": "", "width": ""},
        {"name": 'b_coef', "class": "", "width": ""},
        {"name": 'is_ipc', "class": "", "width": ""},
        {"name": 'species', "class": "", "width": ""},
    ]


class AssayUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.Assay
    form_class = forms.AssayForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Assay"), "url": reverse_lazy("edna:assay_list")}
    container_class = "container curvy"


class AssayCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.Assay
    form_class = forms.AssayForm
    success_url = reverse_lazy('edna:assay_list')
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Assay"), "url": reverse_lazy("edna:assay_list")}
    container_class = "container curvy"


class AssayDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Assay
    template_name = 'edna/assay_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Assay"), "url": reverse_lazy("edna:assay_list")}
    container_class = "container curvy"
    field_list = [
        "alias",
        "lod",
        "loq",
        "a_coef",
        "b_coef",
        "is_ipc",
        "species",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AssayDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.Assay
    success_url = reverse_lazy('edna:assay_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container curvy"


# COLLECTIONS #
###############

class CollectionListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.Collection
    template_name = 'edna/list.html'
    filterset_class = filters.CollectionFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:collection_detail"
    new_object_url = reverse_lazy("edna:collection_new")
    new_btn_text = gettext_lazy("Add a New Project")
    container_class = "container-fluid curvy"
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'name', "class": "", "width": ""},
        {"name": 'dates|{}'.format(_("collection dates")), "class": "", "width": ""},
        {"name": 'region', "class": "", "width": ""},
        {"name": 'description', "class": "", "width": ""},
        {"name": 'province', "class": "", "width": ""},
        {"name": 'sample_count|{}'.format(_("sample count")), "class": "", "width": ""},
        {"name": 'fiscal_year', "class": "", "width": ""},
    ]


class CollectionUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.Collection
    form_class = forms.CollectionForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:collection_detail", args=[self.get_object().id])}


class CollectionCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.Collection
    form_class = forms.CollectionForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container curvy"


class CollectionDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Collection
    template_name = 'edna/collection_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container-fluid"

    def get_field_list(self):
        return utils.get_collection_field_list(self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["sample_labels"] = get_labels(models.Sample)
        context["filter_labels"] = get_labels(models.Filter)
        context["extract_labels"] = get_labels(models.DNAExtract)
        context["pcr_labels"] = get_labels(models.PCR)
        context["pcr_assay_labels"] = get_labels(models.PCRAssay)

        return context


class CollectionDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.Collection
    success_url = reverse_lazy('edna:collection_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container curvy"
    grandparent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}
    delete_protection = False

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:collection_detail", args=[self.get_object().id])}


class ImportSamplesView(eDNAAdminRequiredMixin, CommonFormView):
    form_class = forms.FileImportForm
    template_name = 'edna/sample_import_form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}
    h1 = ' '
    container_class = "container-fluid"
    active_page_name_crumb = gettext_lazy("Sample CSV Import")

    def get_parent_crumb(self):
        return {"title": self.get_collection(), "url": reverse("edna:collection_detail", args=[self.get_collection().id])}

    def get_collection(self):
        return get_object_or_404(models.Collection, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        example_obj = list()
        url = "http://" + get_current_site(self.request).domain + static("edna/sample_import_template.csv")
        r = requests.get(url)
        csv_reader = csv.DictReader(r.text.splitlines())
        for row in csv_reader:
            example_obj.append(row)
        context["example_obj"] = example_obj
        context["sample_types"] = models.SampleType.objects.all().order_by("id")
        return context

    def form_valid(self, form):
        my_object = self.get_collection()
        temp_file = form.files['temp_file']
        temp_file.seek(0)
        csv_reader = csv.DictReader(StringIO(temp_file.read().decode('utf-8')))
        for row in csv_reader:
            bottle_id = row["bottle_id"]
            sample_type = row["sample_type"]
            location = row["location"]
            site = row["site"]
            station = row["station"]
            samplers = row["samplers"]
            datetime = make_aware(dt.datetime.strptime(row["datetime"], "%m/%d/%Y %H:%M"), timezone=timezone.get_current_timezone())
            latitude = nz(row["latitude"], None)
            longitude = nz(row["longitude"], None)
            comments = row["comments"]

            sample, create = models.Sample.objects.get_or_create(bottle_id=bottle_id, collection=my_object, sample_type_id=sample_type)
            sample.location = location
            sample.site = site
            sample.station = station
            sample.samplers = samplers
            sample.datetime = datetime
            sample.latitude = latitude
            sample.longitude = longitude
            sample.comments = comments
            sample.save()

        return HttpResponseRedirect(self.get_parent_crumb()["url"])


class SampleDataEntryTemplateView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Collection
    template_name = 'edna/sample_data_entry.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}
    h1 = ' '
    container_class = "container-fluid"
    active_page_name_crumb = gettext_lazy("Data Entry")

    def get_parent_crumb(self):
        return {"title": self.get_collection(), "url": reverse("edna:collection_detail", args=[self.get_collection().id])}

    def get_collection(self):
        return get_object_or_404(models.Collection, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        example_obj = list()
        url = "http://" + get_current_site(self.request).domain + static("edna/sample_import_template.csv")
        r = requests.get(url)
        csv_reader = csv.DictReader(r.text.splitlines())
        for row in csv_reader:
            example_obj.append(row)
        context["example_obj"] = example_obj
        return context


# FILES #
#########

class FileCreateView(eDNAAdminRequiredMixin, CommonPopoutCreateView):
    model = models.File
    form_class = forms.FileForm
    is_multipart_form_data = True

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.collection_id = self.kwargs['collection']
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class FileUpdateView(eDNAAdminRequiredMixin, CommonPopoutUpdateView):
    model = models.File
    form_class = forms.FileForm
    is_multipart_form_data = True


class FileDeleteView(eDNAAdminRequiredMixin, CommonPopoutDeleteView):
    model = models.File


# SAMPLES #
###########

##########

class SampleListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.Sample
    template_name = 'edna/list.html'
    filterset_class = filters.SampleFilter
    paginate_by = 50
    home_url_name = "edna:index"
    row_object_url_name = "edna:sample_detail"
    container_class = "container-fluid curvy"
    field_list = [
        {"name": 'display|sample ID', "class": "", "width": ""},
        {"name": 'sample_type', "class": "", "width": ""},
        {"name": 'bottle_id', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'location', "class": "", "width": ""},
        {"name": 'station', "class": "", "width": ""},
        {"name": 'site', "class": "", "width": ""},
        {"name": 'coordinates', "class": "", "width": ""},
        {"name": 'filter_count|{}'.format(gettext_lazy("filters")), "class": "", "width": ""},
        {"name": 'extract_count|{}'.format(gettext_lazy("extractions")), "class": "", "width": ""},
        {"name": 'pcr_count|{}'.format(gettext_lazy("PCRs")), "class": "", "width": ""},
        {"name": 'assay_count|{}'.format(gettext_lazy("assays tested")), "class": "", "width": ""},
    ]


class SampleCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    container_class = "container curvy"
    grandparent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}

    def get_cancel_url(self):
        return self.get_parent_crumb().get("url")

    def get_initial(self):
        return dict(add_another=True, collection_date=timezone.now())

    def get_collection(self):
        return get_object_or_404(models.Collection, pk=self.kwargs.get("collection"))

    def get_parent_crumb(self):
        return {"title": self.get_collection(), "url": reverse("edna:collection_detail", args=[self.get_collection().id])}

    def get_success_url(self):
        return self.get_parent_crumb()["url"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        collection = self.get_collection()
        obj.collection = collection
        obj.save()
        if form.cleaned_data.get("add_another", False):
            return HttpResponseRedirect(reverse("edna:sample_new", args=[collection.id]))
        else:
            return HttpResponseRedirect(self.get_success_url())


class SampleUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    greatgrandparent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("edna:sample_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        return {"title": self.get_object().collection, "url": reverse_lazy("edna:collection_detail", args=[self.get_object().collection.id])}


class SampleDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.Sample
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container curvy"
    home_url_name = "edna:index"
    greatgrandparent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("edna:sample_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        return {"title": self.get_object().collection, "url": reverse_lazy("edna:collection_detail", args=[self.get_object().collection.id])}

    def get_success_url(self):
        return self.get_grandparent_crumb().get("url")


class SampleDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Sample
    template_name = 'edna/sample_detail.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Projects"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container-fluid"
    field_list = [
        'display|sample Id',
        "sample_type",
        'bottle_id',
        "location",
        "site",
        "station",
        'datetime',
        'samplers',
        'coordinates',
        'comments',
        'metadata',
    ]

    def get_parent_crumb(self):
        return {"title": self.get_object().collection, "url": reverse("edna:collection_detail", args=[self.get_object().collection.id])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assay_field_list"] = utils.get_assay_field_list()
        return context


# FILTRATION BATCHES #
######################

class FiltrationBatchListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.FiltrationBatch
    template_name = 'edna/list.html'
    filterset_class = filters.FiltrationBatchFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:filtration_batch_detail"
    new_object_url = reverse_lazy("edna:filtration_batch_new")
    new_btn_text = gettext_lazy("Add a New Filtration Batch")
    container_class = "container-fluid curvy"
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'operators', "class": "", "width": ""},
        {"name": 'default_collection', "class": "", "width": ""},
        {"name": 'comments', "class": "", "width": ""},
        {"name": 'filter_count|{}'.format(gettext_lazy("filters")), "class": "", "width": ""},
    ]


class FiltrationBatchUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.FiltrationBatch
    form_class = forms.FiltrationBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}
    container_class = "container curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:filtration_batch_detail", args=[self.get_object().id])}


class FiltrationBatchCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.FiltrationBatch
    form_class = forms.FiltrationBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}
    container_class = "container curvy"


class FiltrationBatchDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.FiltrationBatch
    template_name = 'edna/filtration_batch_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}
    container_class = "container-fluid"
    field_list = utils.get_batch_field_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_field_list = [
            'bottle_id',
            'datetime',
            'site_identifier',
            'coordinates',
            # 'observation_count|{}'.format(_("lobster count")),
        ]
        context["sample_field_list"] = sample_field_list
        return context


class FiltrationBatchDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.FiltrationBatch
    success_url = reverse_lazy('edna:filtration_batch_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container curvy"
    grandparent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}
    delete_protection = False

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:filtration_batch_detail", args=[self.get_object().id])}


# EXTRACTION BATCHES #
######################

class ExtractionBatchListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.ExtractionBatch
    template_name = 'edna/list.html'
    filterset_class = filters.ExtractionBatchFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:extraction_batch_detail"
    new_object_url = reverse_lazy("edna:extraction_batch_new")
    new_btn_text = gettext_lazy("Add a New Extraction Batch")
    container_class = "container-fluid curvy"
    h1 = gettext_lazy("DNA Extraction Batches")
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'operators', "class": "", "width": ""},
        {"name": 'default_collection', "class": "", "width": ""},
        {"name": 'comments', "class": "", "width": ""},
        {"name": 'extract_count|{}'.format(gettext_lazy("Extractions")), "class": "", "width": ""},

    ]


class ExtractionBatchUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.ExtractionBatch
    form_class = forms.ExtractionBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}
    container_class = "container curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:extraction_batch_detail", args=[self.get_object().id])}


class ExtractionBatchCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.ExtractionBatch
    form_class = forms.ExtractionBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}
    container_class = "container curvy"


class ExtractionBatchDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.ExtractionBatch
    template_name = 'edna/extraction_batch_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}
    container_class = "container-fluid"
    field_list = utils.get_batch_field_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_field_list = [
            'bottle_id',
            'datetime',
            'site_identifier',
            'coordinates',
            # 'observation_count|{}'.format(_("lobster count")),
        ]
        context["sample_field_list"] = sample_field_list
        return context


class ExtractionBatchDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.ExtractionBatch
    success_url = reverse_lazy('edna:extraction_batch_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container curvy"
    grandparent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}
    delete_protection = False

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:extraction_batch_detail", args=[self.get_object().id])}


# PCR BATCHES #
######################

class PCRBatchListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.PCRBatch
    template_name = 'edna/list.html'
    filterset_class = filters.PCRBatchFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:pcr_batch_detail"
    new_object_url = reverse_lazy("edna:pcr_batch_new")
    new_btn_text = gettext_lazy("Add a New PCR Batch")
    container_class = "container-fluid curvy"
    h1 = gettext_lazy("qPCR Batches")
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'operators', "class": "", "width": ""},
        {"name": 'default_collection', "class": "", "width": ""},
        {"name": 'plate_id', "class": "", "width": ""},
        {"name": 'machine_number', "class": "", "width": ""},
        {"name": 'run_program', "class": "", "width": ""},
        {"name": 'control_status', "class": "", "width": ""},
        {"name": 'comments', "class": "", "width": ""},
        {"name": 'pcr_count|{}'.format(gettext_lazy("PCRs")), "class": "", "width": ""},
    ]

    def get_extra_button_dict1(self):
        return {
            "name": _("Import from Template"),
            "url": reverse("edna:import_pcrs"),
            "class": "btn-outline-dark",
        }


class PCRBatchUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.PCRBatch
    form_class = forms.PCRBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    container_class = "container curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:pcr_batch_detail", args=[self.get_object().id])}


class PCRBatchCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.PCRBatch
    form_class = forms.PCRBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    container_class = "container curvy"


class PCRBatchDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.PCRBatch
    template_name = 'edna/pcr_batch_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    container_class = "container-fluid"
    field_list = utils.get_pcr_batch_field_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PCRBatchDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.PCRBatch
    success_url = reverse_lazy('edna:pcr_batch_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container curvy"
    grandparent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    delete_protection = False

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:pcr_batch_detail", args=[self.get_object().id])}


# Filters #
###########

class FilterListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.Filter
    template_name = 'edna/list.html'
    filterset_class = filters.FilterFilter
    paginate_by = 50
    home_url_name = "edna:index"
    row_object_url_name = "edna:filter_detail"
    container_class = "container-fluid curvy"
    field_list = [
        {"name": 'display|filter ID', "class": "", "width": ""},
        {"name": 'filtration_batch', "class": "", "width": ""},
        {"name": 'sample', "class": "", "width": ""},
        {"name": 'tube_id', "class": "", "width": ""},
        {"name": 'start_datetime', "class": "", "width": ""},
        {"name": 'storage_location', "class": "", "width": ""},
        {"name": 'extract_count|{}'.format(gettext_lazy("extractions")), "class": "", "width": ""},
        {"name": 'pcr_count|{}'.format(gettext_lazy("PCRs")), "class": "", "width": ""},
        {"name": 'assay_count|{}'.format(gettext_lazy("assays tested")), "class": "", "width": ""},
    ]


class FilterDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Filter
    template_name = 'edna/filter_detail.html'
    home_url_name = "edna:index"
    container_class = "container curvy"
    field_list = [
        'display|filter Id',
        "filtration_batch",
        "sample",
        "tube_id",
        "filtration_type",
        "start_datetime",
        "duration_min",
        "filtration_volume_ml",
        "storage_location",
        "filtration_ipc",
        "comments",
        'metadata',
    ]

    def get_parent_crumb(self):
        return {"title": self.get_object().filtration_batch, "url": reverse("edna:filter_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assay_field_list"] = utils.get_assay_field_list()
        return context


# DNAExtracts #
###########

class DNAExtractListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.DNAExtract
    template_name = 'edna/list.html'
    filterset_class = filters.DNAExtractFilter
    paginate_by = 50
    home_url_name = "edna:index"
    row_object_url_name = "edna:extract_detail"
    container_class = "container-fluid curvy"
    field_list = [
        {"name": 'display|extract ID', "class": "", "width": ""},
        {"name": 'extraction_batch', "class": "", "width": ""},
        {"name": 'filter', "class": "", "width": ""},
        {"name": 'extraction_number', "class": "", "width": ""},
        {"name": 'start_datetime', "class": "", "width": ""},
        {"name": 'storage_location', "class": "", "width": ""},
        {"name": 'pcr_count|{}'.format(gettext_lazy("PCRs")), "class": "", "width": ""},
        {"name": 'assay_count|{}'.format(gettext_lazy("assays tested")), "class": "", "width": ""},
    ]


class DNAExtractDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.DNAExtract
    template_name = 'edna/filter_detail.html'
    home_url_name = "edna:index"
    container_class = "container curvy"
    field_list = [
        'display|extract Id',
        "extraction_batch",
        "filter",
        "sample",
        "extraction_number",
        "start_datetime",
        "dna_extraction_protocol",
        "storage_location",
        "extraction_plate_id",
        "extraction_plate_well",
        "comments",
        'metadata',

    ]

    def get_parent_crumb(self):
        return {"title": self.get_object().extraction_batch, "url": reverse("edna:extract_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assay_field_list"] = utils.get_assay_field_list()
        return context


# PCRs #
###########

class PCRListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.PCR
    template_name = 'edna/list.html'
    filterset_class = filters.PCRFilter
    paginate_by = 50
    home_url_name = "edna:index"
    row_object_url_name = "edna:pcr_detail"
    container_class = "container-fluid curvy"
    field_list = [
        {"name": 'display|qPCR ID', "class": "", "width": ""},
        {"name": 'pcr_batch', "class": "", "width": ""},
        {"name": 'assay_count|{}'.format(gettext_lazy("assays tested")), "class": "", "width": ""},
    ]


class PCRDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.PCR
    template_name = 'edna/filter_detail.html'
    home_url_name = "edna:index"
    container_class = "container curvy"
    field_list = [
        'display|pcr Id',
        "pcr_batch",
        "sample",
        "filter",
        "extract",
        "pcr_plate_well",
        "master_mix",
        "comments",
        'metadata',
    ]

    def get_parent_crumb(self):
        return {"title": self.get_object().pcr_batch, "url": reverse("edna:pcr_list")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assay_field_list"] = utils.get_assay_field_list()
        return context


# REPORTS #
###########

class ReportSearchFormView(eDNAAdminRequiredMixin, CommonFormView):
    template_name = 'edna/report_search.html'
    form_class = forms.ReportSearchForm
    h1 = gettext_lazy("eDNA Reports")

    def form_valid(self, form):
        report = int(form.cleaned_data["report"])
        year = nz(form.cleaned_data["year"], "None")
        # if report == 1:
        #     return HttpResponseRedirect(reverse("edna:sample_log_report") + f"?year={year}")
        # else:
        messages.error(self.request, "Report is not available. Please select another report.")
        return HttpResponseRedirect(reverse("edna:reports"))


def export_pcr_batch_csv(request, pk):
    return reports.generate_pcr_batch_csv(pk)


#
# @login_required()
# def sample_log_report(request):
#     year = None if not request.GET.get("year") or request.GET.get("year") == "None" else int(request.GET.get("year"))
#     file_url = reports.generate_sample_log(year=year)
#
#     if os.path.exists(file_url):
#         with open(file_url, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = f'inline; filename="sample log ({timezone.now().strftime("%Y-%m-%d")}).xlsx"'
#
#             return response
#     raise Http404


class ImportPCRView(eDNAAdminRequiredMixin, CommonFormView):
    form_class = forms.FileImportForm
    template_name = 'edna/pcr_batch_import_form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    h1 = ' '
    active_page_name_crumb = "import"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["master_mixes"] = models.MasterMix.objects.all()
        context["assays"] = models.Assay.objects.all()
        return context

    def form_valid(self, form):
        temp_file = form.files['temp_file']
        temp_file.seek(0)
        year = None
        month = None
        day = None
        hour = None
        minute = None
        header_row = None
        batch = None

        for row in csv.reader(StringIO(temp_file.read().decode('utf-8'))):
            if not header_row:
                if len(row):
                    if row[0] == "batch_id":
                        try:
                            batch = models.PCRBatch.objects.get(pk=row[1])
                            batch.pcrs.all().delete()
                        except:
                            pass
                    if batch:
                        if row[0] == "year": year = row[1] if row[1] and row[1] != "" else None
                        if row[0] == "month": month = row[1] if row[1] and row[1] != "" else None
                        if row[0] == "day": day = row[1] if row[1] and row[1] != "" else None
                        if row[0] == "hour": hour = row[1] if row[1] and row[1] != "" else 12
                        if row[0] == "minute": minute = row[1] if row[1] and row[1] != "" else 0
                        if row[0] == "comments": batch.comments = row[1]
                        if row[0] == "plate_id": batch.plate_id = row[1]
                        if row[0] == "machine_number": batch.machine_number = row[1]
                        if row[0] == "run_program": batch.run_program = row[1]
            else:
                # start by clearing all the existing pcrs in the pcr batch
                if not batch:
                    messages.warning(self.request, f'This file is missing a reference to a valid PCR batch ID')
                    return HttpResponseRedirect(reverse("edna:pcr_batch_list"))
                else:

                    # construct row dict
                    row_dict = dict()
                    for i in range(0, len(header_row)):
                        val = row[i] if len(row[i]) and nz(row[i], None) else None
                        row_dict[header_row[i]] = val

                    # only do something if ct value
                    ct = row_dict["ct"]
                    if ct:

                        # start with PCR details
                        extraction_number = row_dict["extraction_number"]
                        master_mix = row_dict["master_mix"]
                        assay = row_dict["assay"]

                        if not extraction_number or not master_mix or not assay:
                            messages.warning(self.request, f'This row is missing some important information and will not be imported: {row_dict}')
                        else:
                            # get the extract object from the extraction number
                            extracts = models.DNAExtract.objects.filter(extraction_number__iexact=extraction_number)
                            if not extracts.exists():
                                messages.warning(self.request, f'cannot find extraction number: {extraction_number}')
                            elif extracts.count() > 1:
                                messages.warning(self.request, f'extraction number is not unique: {extraction_number}')
                            elif batch.default_collection != extracts.first().collection:
                                messages.warning(self.request, f'extraction number is from another project: {extraction_number}')
                            else:
                                extract = extracts.first()

                                # get the master mix
                                mixes = models.MasterMix.objects.filter(name__iexact=master_mix)
                                if not mixes.exists():
                                    messages.warning(self.request, f'cannot find master mix: {master_mix}')
                                else:
                                    master_mix = mixes.first()

                                    # get the assay
                                    assays = models.Assay.objects.filter(alias__iexact=assay)
                                    if not assays.exists():
                                        messages.warning(self.request, f'cannot find assay alias: {assay}')
                                    else:
                                        assay = assays.first()

                                        # now we can get / create the pcr object
                                        pcr = models.PCR.objects.get_or_create(
                                            pcr_batch=batch,
                                            master_mix=master_mix,
                                            extract=extract,
                                            pcr_plate_well=row_dict["pcr_plate_well"]
                                        )[0]

                                        pcr.save() # populate the collection

                                        # now finally, the assay itself
                                        try:
                                            ct = float(ct)
                                            is_undetermined = False
                                        except Exception as e:
                                            print(e)
                                            is_undetermined = True
                                            ct = None

                                        assay = models.PCRAssay.objects.create(
                                            pcr=pcr,
                                            assay=assay,
                                            ct=ct,
                                            is_undetermined=is_undetermined,
                                            threshold=row_dict["threshold"]
                                        )

            # if we run into the first header of the assay table, turn off the "wait" flag
            if len(row) and row[0] == "extraction_number":
                header_row = row
        #
        #
        #             extraction_number = nz(row[0], None)
        #             extraction_number = nz(row[0], None)
        #
        #
        #
        #
        #         # the results
        #         threshold = nz(row[6], None)
        #         ct = nz(row[7], None)
        #         comments = nz(row[8], None)
        #
        #         # we should be able to get an assay from the unique_id
        #         # # pcr_assay = get_object_or_404(models.PCRAssay, pk=unique_id)
        #         # # pcr = pcr_assay.pcr
        #         # # pcr.pcr_plate_well = pcr_plate_well
        #         # # every row will correspond to a pcr assay
        #         #
        #         # #  let's see if we can associate an extract id
        #         # # if extract:
        #         # #     # prioritize the extract id field
        #         # #     extracts = models.DNAExtract.objects.filter(id=extract.replace("x", ""))
        #         # #     if extracts.exists():
        #         # #         pcr.extract = extracts.first()
        #         # #     else:
        #         # #         messages.warning(self.request, f'cannot find extract id: {extract}')
        #         # #     # try again with extraction number
        #         # # elif extraction_number:
        #         # #     extracts = models.DNAExtract.objects.filter(extraction_number__iexact=extraction_number)
        #         # #     if extracts.exists():
        #         # #         pcr.extract = extracts.first()
        #         # #     else:
        #         # #         messages.warning(self.request, f'cannot find extraction number: {extraction_number}')
        #         # # # master mix
        #         # # if master_mix:
        #         # #     mixes = models.MasterMix.objects.filter(name__iexact=master_mix)
        #         # #     if mixes.exists():
        #         # #         pcr.master_mix = mixes.first()
        #         # #     else:
        #         # #         messages.warning(self.request, f'cannot find master mix: {master_mix}')
        #         # pcr.save()
        #         #
        #         #
        #         # # assay
        #         # # if assay:
        #         # #     assays = models.Assay.objects.filter(alias__iexact=assay)
        #         # #     if assays.exists():
        #         # #         pcr_assay.assay = assays.first()
        #         # #     else:
        #         # #         messages.warning(self.request, f'cannot find assay alias: {assay}')
        #         #
        #         # # threshold
        #         # pcr_assay.threshold = threshold
        #         #
        #         # if ct:
        #         #     if ct.lower() in ["na", "undetermined", "unknown"]:
        #         #         pcr_assay.is_undetermined = True
        #         #     else:
        #         #         try:
        #         #             ct = float(ct)
        #         #         except Exception as e:
        #         #             print(e)
        #         #             ct = None
        #         #         pcr_assay.ct = ct
        #         #
        #         # pcr_assay.comments = comments
        #         #
        #         # try:
        #         #     pcr_assay.save()
        #         # except Exception as e:
        #         #     messages.error(self.request, e)
        #

        #
        if year and month and day:
            batch.datetime = timezone.datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=timezone.now().tzinfo)
        # batch.save()
        # batch.operators.add(self.request.user)

        return HttpResponseRedirect(reverse("edna:pcr_batch_detail", args=[batch.id]))
