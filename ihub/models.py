import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from markdown import markdown

from lib.functions.custom_functions import listrify
from lib.functions.custom_functions import nz
from masterlist import models as ml_models
from shared_models import models as shared_models
from shared_models.models import SimpleLookup
# This can be delete after the next time migrations are crushed
from shared_models.utils import get_metadata_string


def audio_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/entry_<id>/<filename>
    return 'ihub/org_{}/{}'.format(instance.id, filename)


NULL_YES_NO_CHOICES = (
    (None, _("---------")),
    (1, _("Yes")),
    (0, _("No")),
)

YES_NO_CHOICES = (
    (True, "Yes"),
    (False, "No"),
)


class iHubUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="ihub_user", verbose_name=_("DM Apps user"))
    is_admin = models.BooleanField(default=False, verbose_name=_("app administrator?"), choices=YES_NO_CHOICES)
    is_crud_user = models.BooleanField(default=False, verbose_name=_("Edit permissions?"), choices=YES_NO_CHOICES)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        ordering = ["-is_admin", "user__first_name", ]


class EntryType(SimpleLookup):
    color = models.CharField(max_length=25, blank=True, null=True)


class Status(SimpleLookup):
    color = models.CharField(max_length=25, blank=True, null=True)


class FundingPurpose(SimpleLookup):
    pass


class FundingProgram(SimpleLookup):
    abbrev_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("abbreviation (French)"))
    abbrev_fre = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("abbreviation (French)"))

    @property
    def full_eng(self):
        return "{} ({})".format(self.name, self.abbrev_eng)

    @property
    def full_fre(self):
        return "{} ({})".format(self.nom, self.abbrev_fre)


class Entry(models.Model):
    # basic
    title = models.CharField(max_length=1000, blank=False, null=True, verbose_name=_("title"))
    location = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("location"))
    proponent = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("proponent"))
    organizations = models.ManyToManyField(ml_models.Organization, related_name="entries", blank=True,
                                           limit_choices_to={'grouping__is_indigenous': True}, verbose_name=_("organizations"))
    initial_date = models.DateTimeField(verbose_name=_("initial activity date"), blank=True, null=True)
    response_requested_by = models.DateTimeField(verbose_name=_("response requested by"), blank=True, null=True)
    anticipated_end_date = models.DateTimeField(verbose_name=_("anticipated end date"), blank=True, null=True)
    is_faa_required = models.BooleanField(null=True, blank=True, verbose_name=_("is an FAA required?"))
    is_faa_issued = models.BooleanField(null=True, blank=True, verbose_name=_("has an FAA been issued?"))
    status = models.ForeignKey(Status, default=1, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("status"),
                               related_name="entries")
    sectors = models.ManyToManyField(ml_models.Sector, blank=True, related_name="entries", verbose_name=_("DFO sectors"))
    entry_type = models.ForeignKey(EntryType, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="entries",
                                   verbose_name=_("Entry Type"))  # title case needed
    regions = models.ManyToManyField(shared_models.Region, related_name="entries", verbose_name=_("regions"))
    response_deadline = models.DateTimeField(verbose_name=_("response deadline"), blank=True, null=True)

    # funding
    funding_program = models.ForeignKey(FundingProgram, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        verbose_name=_("funding program"), related_name="entries")
    fiscal_year = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("fiscal year/multiyear"))
    funding_needed = models.IntegerField(blank=True, null=True, choices=NULL_YES_NO_CHOICES, verbose_name=_("is funding needed?"))
    funding_purpose = models.ForeignKey(FundingPurpose, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        verbose_name=_("funding purpose"), related_name="entries")
    amount_requested = models.FloatField(blank=True, null=True, verbose_name=_("funding requested"))  # title case needed
    amount_approved = models.FloatField(blank=True, null=True, verbose_name=_("funding approved"))
    amount_transferred = models.FloatField(blank=True, null=True, verbose_name=_("amount transferred"))
    amount_lapsed = models.FloatField(blank=True, null=True, verbose_name=_("amount lapsed"))
    amount_owing = models.IntegerField(blank=True, null=True, choices=NULL_YES_NO_CHOICES,
                                       verbose_name=_("does any funding need to be recovered?"))

    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_("date created"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("created by"),
                                   related_name="user_entries")
    old_id = models.IntegerField(blank=True, null=True, editable=False, unique=True)  # used for importing new data.

    @property
    def has_funding_detail(self):
        return self.funding_program or self.fiscal_year or self.funding_needed or \
               self.funding_purpose or self.amount_requested or self.amount_approved or \
               self.amount_transferred or self.amount_lapsed or self.amount_owing

    class Meta:
        ordering = ['-date_created', ]

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        # self.fiscal_year = fiscal_year(date=self.initial_date)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ihub:entry_detail', kwargs={'pk': self.pk})

    @property
    def amount_outstanding(self):
        return nz(self.amount_approved, 0) - nz(self.amount_transferred, 0) - nz(self.amount_lapsed, 0)

    @property
    def followups(self):
        return self.notes.filter(type=4)

    @property
    def other_notes(self):
        return self.notes.filter(~Q(type__in=[4]))

    @property
    def orgs_str(self):
        return listrify([org for org in self.organizations.all()])

    @property
    def sectors_str(self):
        return listrify([sec for sec in self.sectors.all()])

    @property
    def metadata(self):
        return get_metadata_string(
            self.date_created,
            self.created_by,
            self.date_last_modified,
            self.last_modified_by,
        )


class EntryPerson(models.Model):
    # Choices for role
    # TODO: test me
    LEAD = 1
    CONTACT = 2
    SUPPORT = 3
    ROLE_CHOICES = (
        (LEAD, _('Lead')),
        (CONTACT, _('Contact')),
        (SUPPORT, _('Support')),
    )
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="people", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("User"), related_name="ihub_entry_people")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name"))
    organization = models.CharField(max_length=50)
    role = models.IntegerField(choices=ROLE_CHOICES, blank=True, null=True, verbose_name=_("role"))

    def __str__(self):
        # get the name; keep in mind this might be NoneObject
        name = "{} {}".format(self.user.first_name, self.user.last_name) if self.user else self.name
        org = self.organization
        role = self.get_role_display() if self.role else None

        my_str = name if name else None

        if org:
            if my_str:
                my_str += " ({})".format(org)
            else:
                my_str = org

        if my_str and role:
            my_str = "{}: {}".format(role.upper(), my_str)

        return my_str

    class Meta:
        ordering = ['role', 'user__first_name', "user__last_name"]


class EntryNote(models.Model):
    # Choices for type
    ACTION = 1
    NEXTSTEP = 2
    COMMENT = 3
    FOLLOWUP = 4
    INTERNAL = 5
    TYPE_CHOICES = (
        (ACTION, _('Action')),
        (NEXTSTEP, _('Next step')),
        (COMMENT, _('Comment')),
        (FOLLOWUP, _('Follow-up (*)')),
        (INTERNAL, _('Internal')),
    )

    entry = models.ForeignKey(Entry, related_name='notes', on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("author"))
    note = models.TextField()
    status = models.ForeignKey(Status, default=1, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("status"),
                               related_name="entry_notes")

    @property
    def metadata(self):
        return get_metadata_string(self.creation_date, self.author, self.modified_date, with_time=False)

    def __str__(self):
        my_str = "{} - {} [STATUS: {}] (Created by {} {} on {})".format(
            self.get_type_display().upper(),
            self.note,
            self.status,
            self.author.first_name if self.author else "n/a",
            self.author.last_name if self.author else "n/a",
            self.creation_date.strftime("%Y-%m-%d"),
        )
        return my_str

    class Meta:
        ordering = ["-creation_date"]

    @property
    def note_html(self):
        if self.note:
            return markdown(self.note)


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/entry_<id>/<filename>
    return 'ihub/entry_{0}/{1}'.format(instance.entry.id, filename)


class File(models.Model):
    caption = models.CharField(max_length=255, verbose_name=_("caption"))
    entry = models.ForeignKey(Entry, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path, verbose_name=_("file"))
    date_uploaded = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date uploaded"))

    class Meta:
        ordering = ['-date_uploaded']

    def __str__(self):
        return self.caption


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
