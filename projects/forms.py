from django import forms
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext as _
from . import models
from . import views
from django.contrib.auth.models import User
from shared_models import models as shared_models

chosen_js = {"class": "chosen-select-contains"}

# Choices for YesNo
YESNO_CHOICES = (
    (1, "Yes"),
    (0, "No"),
)

class NewProjectForm(forms.ModelForm):
    region = forms.ChoiceField()
    division = forms.ChoiceField()
    field_order = ['year', 'project_title', 'region', 'division', 'section']

    class Meta:
        model = models.Project
        fields = [
            'year',
            'project_title',
            'section',
            'last_modified_by',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'project_title': forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        region_choices = views.get_region_choices(all=True)
        region_choices.insert(0, tuple((None, "---")))
        division_choices = views.get_division_choices(all=True)
        division_choices.insert(0, tuple((None, "---")))
        section_choices = views.get_section_choices(all=True)
        section_choices.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['region'].choices = region_choices

        # even though these are overwritten by js scripts you have to define these so that the validation kicks in properly
        self.fields['division'].choices = division_choices
        self.fields['section'].choices = section_choices


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = [
            'submitted',
            'date_last_modified',
            'section_head_feedback',
            'section_head_approved',
            'manager_feedback',
            'manager_approved',
            'rds_feedback',
            'rds_approved',
        ]
        class_editable = {"class": "editable"}
        widgets = {
            "project_title": forms.Textarea(attrs={"rows": "3"}),

            "description": forms.Textarea(attrs=class_editable),
            "priorities": forms.Textarea(attrs=class_editable),
            "deliverables": forms.Textarea(attrs=class_editable),
            "data_collection": forms.Textarea(attrs=class_editable),
            "data_sharing": forms.Textarea(attrs=class_editable),
            "data_storage": forms.Textarea(attrs=class_editable),
            "regional_dm_needs": forms.Textarea(attrs=class_editable),
            "sectional_dm_needs": forms.Textarea(attrs=class_editable),
            "vehicle_needs": forms.Textarea(attrs=class_editable),
            "it_needs": forms.Textarea(attrs=class_editable),
            "chemical_needs": forms.Textarea(attrs=class_editable),
            "ship_needs": forms.Textarea(attrs=class_editable),
            "feedback": forms.Textarea(attrs=class_editable),

            'start_date': forms.DateInput(attrs={"type": "date"}),
            'end_date': forms.DateInput(attrs={"type": "date"}),
            'last_modified_by': forms.HiddenInput(),
            "section": forms.Select(attrs=chosen_js),
            "program": forms.Select(attrs=chosen_js),
            "responsibility_center": forms.Select(attrs=chosen_js),
            "allotment_code": forms.Select(attrs=chosen_js),
            "existing_project_code": forms.Select(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        SECTION_CHOICES = views.get_section_choices(all=True)
        SECTION_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['section'].choices = SECTION_CHOICES


class ProjectSubmitForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'submitted',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'submitted': forms.HiddenInput(),
        }

class SectionApprovalForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'section_head_feedback',
            'section_head_approved',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'section_head_approved': forms.HiddenInput(),
        }

class DivisionApprovalForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'manager_feedback',
            'manager_approved',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'manager_approved': forms.HiddenInput(),
        }

class BranchApprovalForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'last_modified_by',
            'rds_feedback',
            'rds_approved',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'rds_approved': forms.HiddenInput(),
        }


class StaffForm(forms.ModelForm):
    save_then_go_OT = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = models.Staff
        fields = "__all__"
        labels = {
            "user": _("DFO User"),
        }
        widgets = {
            'project': forms.HiddenInput(),
            'overtime_description': forms.Textarea(attrs={"rows": 5}),
            'user': forms.Select(attrs=chosen_js),
        }


class CollaboratorForm(forms.ModelForm):
    class Meta:
        model = models.Collaborator
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class AgreementForm(forms.ModelForm):
    class Meta:
        model = models.CollaborativeAgreement
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class OMCostForm(forms.ModelForm):
    class Meta:
        model = models.OMCost
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class CapitalCostForm(forms.ModelForm):
    class Meta:
        model = models.CapitalCost
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class GCCostForm(forms.ModelForm):
    class Meta:
        model = models.GCCost
        fields = "__all__"
        widgets = {
            'project': forms.HiddenInput(),
        }


class FYForm(forms.Form):
    fiscal_year = forms.ChoiceField(required=True)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(
            reverse("projects:report_sh", kwargs={"fiscal_year": fy.id, "user": user}), str(fy)) for fy in
            shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        fy_choices.insert(0, (None, "-----"))

        self.fields["fiscal_year"].choices = fy_choices


class ReportSearchForm(forms.Form):
    REPORT_CHOICES = (
        (None, "-----"),
        (3, "Project Summary Report (PDF)"),
        (2, "Batch Workplan Export (PDF) (submitted and approved)"),
        (1, "Master spreadsheet (XLSX)"),
    )
    fiscal_year = forms.ChoiceField(required=True)
    report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    region = forms.MultipleChoiceField(required=False, label="Regions (Leave blank to select all)")
    division = forms.MultipleChoiceField(required=False, label="Divisions (Leave blank to select all)")
    section = forms.MultipleChoiceField(required=False, label="Sections (Leave blank to select all)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fy_choices = [(fy.id, str(fy)) for fy in shared_models.FiscalYear.objects.all() if fy.projects.count() > 0]
        fy_choices.insert(0, (None, "-----"))
        self.fields['region'].choices = views.get_region_choices()
        self.fields['division'].choices = views.get_division_choices()
        self.fields["section"].choices = views.get_section_choices()
        self.fields["fiscal_year"].choices = fy_choices


class OTForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = ["overtime_hours", "overtime_description"]
        widgets = {
            'overtime_hours': forms.HiddenInput(),
            'overtime_description': forms.HiddenInput(),
        }


class UserCreateForm(forms.Form):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    email1 = forms.EmailField(label=_("Email"))
    email2 = forms.EmailField(label=_("Confirm email address"))

    def clean_email1(self):
        new_email = self.cleaned_data['email1']
        # check to make sure is not a duplicate
        if User.objects.filter(email__iexact=new_email).count() > 0:
            raise forms.ValidationError("This email address already exists in the database.")
        # check to make sure is a DFO email
        if new_email.lower().endswith("@dfo-mpo.gc.ca") == False:
            raise forms.ValidationError(_("The email address provided must be a DFO email address."))

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return new_email

    def clean(self):
        cleaned_data = super().clean()
        first_email = cleaned_data.get("email1")
        second_email = cleaned_data.get("email2")

        if first_email and second_email:
            # Only do something if both fields are valid so far.

            # verify the two emails are the same
            if first_email.lower() != second_email.lower():
                raise forms.ValidationError(_("Please make sure the two email addresses provided match."))
