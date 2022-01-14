from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy, gettext

from . import models

chosen_js = {"class": "chosen-select-contains"}


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        exclude = [
            'shortish_name',
            'full_name',
            'full_name_ver1',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),
            'admin': forms.Select(attrs=chosen_js),

        }

    def __init__(self, *args, **kwargs):
        USER_CHOICES = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        User.objects.all().order_by("last_name", "first_name")]
        USER_CHOICES.insert(0, tuple((None, "---")))

        DIVISION_CHOICES = [(obj.id, "{} - {}".format(obj.branch, obj.name)) for obj in
                            models.Division.objects.all().order_by("branch__region", "branch", "name")]
        DIVISION_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['head'].choices = USER_CHOICES
        self.fields['division'].choices = DIVISION_CHOICES


class DivisionForm(forms.ModelForm):
    class Meta:
        model = models.Division
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),
            'admin': forms.Select(attrs=chosen_js),
        }

    def __init__(self, *args, **kwargs):
        BRANCH_CHOICES = [(obj.id, "{} - {}".format(obj.region, obj.name)) for obj in
                          models.Branch.objects.all().order_by("region", "name")]
        BRANCH_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['branch'].choices = BRANCH_CHOICES


class BranchForm(forms.ModelForm):
    class Meta:
        model = models.Branch
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),
            'admin': forms.Select(attrs=chosen_js),
        }

class SectorForm(forms.ModelForm):
    class Meta:
        model = models.Sector
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),
            'admin': forms.Select(attrs=chosen_js),
        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = models.Region
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),
            'head': forms.Select(attrs=chosen_js),
            'admin': forms.Select(attrs=chosen_js),
        }


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = "__all__"


class UserCreateForm(forms.Form):
    first_name = forms.CharField(label=gettext_lazy("First name"))
    last_name = forms.CharField(label=gettext_lazy("Last name"))
    email1 = forms.EmailField(label=gettext_lazy("Email"), help_text=gettext_lazy("Please make sure this is the correct email address, as listed in the DFO Active Directory."))
    email2 = forms.EmailField(label=gettext_lazy("Confirm email address"))
    send_email = forms.BooleanField(required=False, label=gettext_lazy("Send a confirmation email to the new user? "),
                                    help_text=gettext_lazy(
                                        "If this is selected, the new user will receive an email with instructions for how to log in. This is the recommended option."))

    def clean_email1(self):
        new_email = self.cleaned_data['email1']
        # check to make sure is not a duplicate
        if User.objects.filter(email__iexact=new_email).count() > 0:
            raise forms.ValidationError(gettext("This email address already exists in the database."))
        # check to make sure is a DFO email
        if new_email.lower().endswith("@dfo-mpo.gc.ca") == False:
            raise forms.ValidationError(gettext("The email address provided must be a DFO email address."))

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
                raise forms.ValidationError(gettext("Please make sure the two email addresses provided match."))


class ScriptForm(forms.ModelForm):
    class Meta:
        model = models.Script
        fields = "__all__"
        widgets = {
            'modified_by': forms.HiddenInput(),
        }


class ResponsibilityCenterForm(forms.ModelForm):
    class Meta:
        model = models.ResponsibilityCenter
        fields = "__all__"
        widgets = {
            "manager": forms.Select(attrs=chosen_js)
        }


class ProjectCodeForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"
