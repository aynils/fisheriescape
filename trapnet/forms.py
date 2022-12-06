from django import forms
from django.forms import modelformset_factory
from django.utils.translation import gettext, gettext_lazy

from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from shared_models.models import River, FishingArea
from . import models, model_choices

attr_fp_date_time = {"class": "fp-date-time", "placeholder": "Select Date and Time.."}
attr_fp_date = {"class": "fp-date", "placeholder": "Click to select a date.."}
multi_select_js = {"class": "multi-select"}
chosen_js = {"class": "chosen-select-contains"}


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = models.Species
        fields = "__all__"


class RiverForm(forms.ModelForm):
    class Meta:
        model = shared_models.River
        fields = "__all__"


class RiverSiteForm(forms.ModelForm):
    class Meta:
        model = models.RiverSite
        fields = "__all__"
        widgets = {
            "latitude_n": forms.NumberInput(attrs={"placeholder": "DD.dddddd", }),
            "longitude_w": forms.NumberInput(attrs={"placeholder": "DD.dddddd", }),
            "directions": forms.Textarea(attrs={"rows": "3", }),
        }


class SampleForm(forms.ModelForm):
    stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.Sample
        fields = "__all__"
        widgets = {
            "site": forms.Select(attrs=chosen_js),
            "monitoring_program": forms.Select(attrs=chosen_js),
            "samplers": forms.Textarea(attrs={"rows": "2", }),
            "notes": forms.Textarea(attrs={"rows": "3", }),
            "time_released": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M:%S"),
            "arrival_date": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M:%S"),
            "departure_date": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M:%S"),
        }
        labels = {
            "percent_cloud_cover": "cloud cover (0-100)"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        site_choices = [(obj.id, f"{obj.river} --> {obj.name} ({nz(obj.province, 'unknown prov.')})") for obj in models.RiverSite.objects.all()]
        site_choices.insert(0, (None, "-----"))
        self.fields["site"].choices = site_choices
        if kwargs.get("instance"):
            del self.fields["sample_type"]


    def clean_percent_cloud_cover(self):
        percent_cloud_cover = self.cleaned_data['percent_cloud_cover']

        if percent_cloud_cover:
            if percent_cloud_cover % 1 != 0:
                self.add_error('percent_cloud_cover', gettext(
                    "Must be an integer!"
                ))
            percent_cloud_cover /= 100
            if percent_cloud_cover > 1:
                self.add_error('percent_cloud_cover', gettext(
                    "Must be between an integer between 0 and 100!"
                ))
        return percent_cloud_cover

    def clean_monitoring_program(self):
        monitoring_program = self.cleaned_data['monitoring_program']

        if not monitoring_program:
            raise forms.ValidationError(
                gettext("You must select a monitoring program!")
            )
        return monitoring_program

    def clean(self):
        cleaned_data = super().clean()

        # make sure departure is after arrival
        arrival_date = cleaned_data.get("arrival_date")
        departure_date = cleaned_data.get("departure_date")
        if arrival_date and departure_date and departure_date < arrival_date:
            self.add_error('departure_date', gettext(
                "The departure date must be after the arrival date!"
            ))

        # make sure the age thresholds make sense
        age_thresh_0_1 = cleaned_data.get("age_thresh_0_1")
        age_thresh_1_2 = cleaned_data.get("age_thresh_1_2")
        age_thresh_parr_smolt = cleaned_data.get("age_thresh_parr_smolt")
        if age_thresh_0_1 and age_thresh_1_2 and age_thresh_1_2 < age_thresh_0_1:
            self.add_error('age_thresh_1_2', gettext(
                "the 1-2 age threshold must be greater than that for the 0-1 age threshold!"
            ))


class EFSampleForm(forms.ModelForm):
    class Meta:
        model = models.EFSample
        fields = "__all__"
        widgets = {
            "time_released": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M:%S"),
        }

    def clean(self):
        cleaned_data = super().clean()

        # make sure site characterization is null or 1
        percent_riffle = cleaned_data.get("percent_riffle")
        percent_run = cleaned_data.get("percent_run")
        percent_flat = cleaned_data.get("percent_flat")
        percent_pool = cleaned_data.get("percent_pool")
        if (percent_riffle or percent_run or percent_flat or percent_pool) and (
                nz(percent_riffle, 0) + nz(percent_run, 0) + nz(percent_flat, 0) + nz(percent_pool, 0) != 100):
            raise forms.ValidationError(
                gettext("Either site characterization must be left null or must equal to 100")
            )

        # make sure substrate characterization is null or 1
        percent_fine = cleaned_data.get("percent_fine")
        percent_sand = cleaned_data.get("percent_sand")
        percent_gravel = cleaned_data.get("percent_gravel")
        percent_pebble = cleaned_data.get("percent_pebble")
        percent_cobble = cleaned_data.get("percent_cobble")
        percent_rocks = cleaned_data.get("percent_rocks")
        percent_boulder = cleaned_data.get("percent_boulder")
        percent_bedrock = cleaned_data.get("percent_bedrock")
        if (percent_fine or percent_sand or percent_gravel or percent_pebble or percent_cobble or percent_rocks or percent_boulder or percent_bedrock) and (
                nz(percent_fine, 0) + nz(percent_sand, 0) + nz(percent_gravel, 0) + nz(percent_pebble, 0) + nz(percent_cobble, 0) + nz(percent_rocks, 0) + nz(
            percent_boulder, 0) + nz(percent_bedrock, 0) != 100):
            raise forms.ValidationError(
                gettext("Either substrate characterization must be left null or must equal to 100")
            )


class TrapnetSampleForm(forms.ModelForm):
    class Meta:
        model = models.TrapnetSample
        fields = "__all__"
        widgets = {
            "time_released": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M:%S"),
        }


class RSTSampleForm(forms.ModelForm):
    class Meta:
        model = models.RSTSample
        fields = "__all__"
        widgets = {
            "time_released": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M:%S"),
        }


class SweepForm(forms.ModelForm):
    class Meta:
        model = models.Sweep
        exclude = "__all__"

    def clean_sweep_number(self):
        sweep_number = self.cleaned_data['sweep_number']
        if (sweep_number != 0.5) and (sweep_number - int(sweep_number) != 0):
            raise forms.ValidationError("The sweep number must be equal to 0.5 or be a factors of 1!")
        return sweep_number


class SpecimenForm(forms.ModelForm):
    class Meta:
        model = models.Specimen
        fields = "__all__"
        widgets = {
            'sample': forms.HiddenInput(),
            'sweep': forms.HiddenInput(),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = "__all__"


class SampleFileForm(forms.ModelForm):
    class Meta:
        model = models.SampleFile
        fields = "__all__"


class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        # (1, "List of samples (trap data) (CSV)"),
        # (2, "List of entries (fish data) (CSV)"),

        (None, ""),
        (None, "RAW DATA"),
        (None, "------------"),
        (1, "sample data export (csv)"),
        (2, "sweep data export (csv)"),
        (3, "specimen data export (csv)"),
        (4, "Atlantic salmon individual specimen event report (csv)"),

        (None, ""),
        (None, "ELECTROFISHING"),
        (None, "------------"),
        (10, "juvenile salmon CSAS report (csv)"),

        (None, ""),
        (None, "OPEN DATA"),
        (None, "------------"),
        (91, "summary by site by year (csv)"),
        (92, "data dictionary (csv)"),
        (93, "species list (csv)"),
        (94, "web mapping service (WMS) report ENGLISH (csv)"),
        (95, "web mapping service (WMS) report FRENCH (csv)"),
    )

    leave_blank_text = gettext_lazy("leave blank for all")
    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    year = forms.CharField(required=False, widget=forms.NumberInput(), label="Year", help_text=leave_blank_text)
    sample_type = forms.ChoiceField(required=False, label="Sample type", help_text=leave_blank_text)
    fishing_areas = forms.MultipleChoiceField(required=False, label="Fishing areas", help_text=leave_blank_text)
    rivers = forms.MultipleChoiceField(required=False, label="Rivers", help_text=leave_blank_text)
    sites = forms.MultipleChoiceField(required=False, label="Sites", help_text=leave_blank_text)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        site_choices = [(obj.id, str(obj)) for obj in models.RiverSite.objects.filter(samples__isnull=False).distinct()]
        self.fields['sites'].choices = site_choices

        river_choices = [(obj.id, str(obj)) for obj in River.objects.filter(sites__samples__isnull=False).distinct()]
        self.fields['rivers'].choices = river_choices

        fa_choices = [(obj.id, str(obj)) for obj in FishingArea.objects.all()]
        self.fields['fishing_areas'].choices = fa_choices
        self.fields['fishing_areas'].widget.attrs = chosen_js

        sample_type_choices = list(model_choices.sample_type_choices)
        sample_type_choices.insert(0, (None, "-----"))
        self.fields['sample_type'].choices = sample_type_choices


class StatusForm(forms.ModelForm):
    class Meta:
        model = models.Status
        fields = "__all__"


StatusFormset = modelformset_factory(
    model=models.Status,
    form=StatusForm,
    extra=1,
)


class SexForm(forms.ModelForm):
    class Meta:
        model = models.Sex
        fields = "__all__"


SexFormset = modelformset_factory(
    model=models.Sex,
    form=SexForm,
    extra=1,
)


class LifeStageForm(forms.ModelForm):
    class Meta:
        model = models.LifeStage
        fields = "__all__"


LifeStageFormset = modelformset_factory(
    model=models.LifeStage,
    form=LifeStageForm,
    extra=1,
)


class OriginForm(forms.ModelForm):
    class Meta:
        model = models.Origin
        fields = "__all__"


OriginFormset = modelformset_factory(
    model=models.Origin,
    form=OriginForm,
    extra=1,
)


class MaturityForm(forms.ModelForm):
    class Meta:
        model = models.Maturity
        fields = "__all__"


MaturityFormset = modelformset_factory(
    model=models.Maturity,
    form=MaturityForm,
    extra=1,
)


class ElectrofisherForm(forms.ModelForm):
    class Meta:
        model = models.Electrofisher
        fields = "__all__"


ElectrofisherFormset = modelformset_factory(
    model=models.Electrofisher,
    form=ElectrofisherForm,
    extra=1,
)


class ReproductiveStatusForm(forms.ModelForm):
    class Meta:
        model = models.ReproductiveStatus
        fields = "__all__"


ReproductiveStatusFormset = modelformset_factory(
    model=models.ReproductiveStatus,
    form=ReproductiveStatusForm,
    extra=1,
)


class FishingAreaForm(forms.ModelForm):
    class Meta:
        model = shared_models.FishingArea
        fields = "__all__"


FishingAreaFormset = modelformset_factory(
    model=shared_models.FishingArea,
    form=FishingAreaForm,
    extra=1,
)


class TrapNetUserForm(forms.ModelForm):
    class Meta:
        model = models.TrapNetUser
        fields = "__all__"
        widgets = {
            'user': forms.Select(attrs=chosen_js),
        }


TrapNetUserFormset = modelformset_factory(
    model=models.TrapNetUser,
    form=TrapNetUserForm,
    extra=1,
)


class MonitoringProgramForm(forms.ModelForm):
    class Meta:
        model = models.MonitoringProgram
        fields = "__all__"


MonitoringProgramFormset = modelformset_factory(
    model=models.MonitoringProgram,
    form=MonitoringProgramForm,
    extra=1,
)


class BiologicalDetailingForm(forms.ModelForm):
    class Meta:
        model = models.BiologicalDetailing
        fields = "__all__"
