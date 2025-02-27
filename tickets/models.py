import os
#
import markdown
import textile
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from lib.functions.custom_functions import fiscal_year
from shared_models import models as shared_models

try:
    from dm_apps import my_conf as local_conf
except (ModuleNotFoundError, ImportError):
    from dm_apps import default_conf as local_conf


def get_name(self):
    return '{} {}'.format(self.first_name, self.last_name)


User.add_to_class("__str__", get_name)


class Tag(models.Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tickets:tag_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['tag']


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))
    color = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Ticket(models.Model):
    # Choices for priority
    HIGH = '1'
    MED = '2'
    LOW = '3'
    WISHLIST = '4'
    URGENT = '5'
    PRIORITY_CHOICES = (
        (HIGH, _('High')),
        (MED, _('Medium')),
        (LOW, _('Low')),
        (WISHLIST, _('Wish List')),
        (URGENT, _('Urgent')),
    )
    request_type_choices = (
        (1, _('Software request / installation')),
        (2, _('System Adoption')),
        (3, _('Database creation')),
        (4, _('Data sharing / publication')),
        (5, _('Process development')),
        (6, _('Hardware')),
        (7, _('Data entry / digitization')),
        (8, _('Permissions')),
        (9, _('Database maintenance')),
        (12, _('Software issue (licensing)')),
        (13, _('Disk recovery')),
        (14, _('Hardware and software')),
        (15, _('Security exemption')),
        (16, _('App development')),
        (17, _('Report development')),
        (18, _('Other')),
        (19, _('App enhancement')),
        (20, _('Bug')),
        (21, _('Quality control element')),
        (22, _('Data transfer')),
        (23, _('New Shiny App')),
    )

    title = models.CharField(max_length=255)
    primary_contact = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    app = models.CharField(max_length=25, default="general", verbose_name=_("application name"), blank=True, null=True)
    dm_assigned = models.ManyToManyField(User, limit_choices_to={"is_staff": True},
                                         verbose_name=_("ticket assigned to"), blank=True, related_name="dm_assigned_tickets")
    request_type = models.IntegerField(verbose_name=_("type of request"), choices=request_type_choices, default=20)
    status = models.ForeignKey(Status, default=2, on_delete=models.DO_NOTHING)
    priority = models.CharField(default='2', max_length=1, choices=PRIORITY_CHOICES, verbose_name=_("priority level"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    notes = models.TextField(blank=True, null=True)
    notes_html = models.TextField(blank=True, null=True, verbose_name="Notes")
    date_opened = models.DateTimeField(default=timezone.now)
    date_closed = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    resolved_email_date = models.DateTimeField(null=True, blank=True, verbose_name="Notification sent to primary contact")
    fiscal_year = models.ForeignKey(shared_models.FiscalYear, blank=True, null=True, on_delete=models.DO_NOTHING)
    github_issue_number = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.notes:
            self.notes_html = markdown.markdown(self.notes)

        self.date_modified = timezone.now()

        # if status is resolved or canceled, add a date closed timestamp
        if self.status_id == 1 or self.status == 4:
            self.date_closed = timezone.now()
        else:
            self.date_closed = None

        self.fiscal_year_id = fiscal_year(self.date_opened, sap_style=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['status', '-date_modified']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tickets:detail', kwargs={'pk': self.id})

    @property
    def description_html(self):
        if self.description:
            return textile.textile(self.description)

    @property
    def sd_description_html(self):
        if self.sd_description:
            return textile.textile(self.sd_description)

    @property
    def app_display(self):
        # choices for app
        APP_DICT = local_conf.APP_DICT
        APP_DICT["tickets"] = dict(name="DM Apps Tickets")
        registered_app = APP_DICT.get(self.app)
        if registered_app:
            if isinstance(registered_app, dict) and registered_app.get("name"):
                registered_app = registered_app["name"]
            return registered_app
        return self.app


class FollowUp(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="follow_ups", on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_("follow up message"))
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="tickets_follow_ups")
    created_date = models.DateTimeField(default=timezone.now)
    github_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return "{} <code>({} {} on {})</code>".format(self.message, self.created_by.first_name, self.created_by.last_name,
                                                      self.created_date.strftime("%Y-%m-%d %H:%M"))


def ticket_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'tickets/ticket_{0}/{1}'.format(instance.ticket.id, filename)


class File(models.Model):
    caption = models.CharField(max_length=255)
    ticket = models.ForeignKey(Ticket, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=ticket_directory_path, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('tickets:file_detail', kwargs={
            'ticket': self.ticket.id,
            'pk': self.id
        })


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
