import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from tracking.managers import VisitorManager, PageviewManager
from tracking.settings import TRACK_USING_GEOIP

try:
    from django.contrib.gis.geoip import HAS_GEOIP
except ImportError:
    from django.contrib.gis.geoip2 import HAS_GEOIP2 as HAS_GEOIP

if HAS_GEOIP:
    try:
        from django.contrib.gis.geoip import GeoIP, GeoIPException
    except ImportError:
        from django.contrib.gis.geoip2 import (
            GeoIP2 as GeoIP,
            GeoIP2Exception as GeoIPException,
        )

GEOIP_CACHE_TYPE = getattr(settings, 'GEOIP_CACHE_TYPE', 4)

log = logging.getLogger(__file__)


class Visitor(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='visit_history',
        null=True,
        editable=False,
        on_delete=models.CASCADE,
    )
    # Update to GenericIPAddress in Django 1.4
    ip_address = models.CharField(max_length=39, editable=False)
    user_agent = models.TextField(null=True, editable=False)
    start_time = models.DateTimeField(default=timezone.now, editable=False)
    expiry_age = models.IntegerField(null=True, editable=False)
    expiry_time = models.DateTimeField(null=True, editable=False)
    time_on_site = models.IntegerField(null=True, editable=False)
    end_time = models.DateTimeField(null=True, editable=False)

    objects = VisitorManager()

    def session_expired(self):
        """The session has ended due to session expiration."""
        if self.expiry_time:
            return self.expiry_time <= timezone.now()
        return False
    session_expired.boolean = True

    def session_ended(self):
        """The session has ended due to an explicit logout."""
        return bool(self.end_time)
    session_ended.boolean = True

    @property
    def geoip_data(self):
        """Attempt to retrieve MaxMind GeoIP data based on visitor's IP."""
        if not HAS_GEOIP or not TRACK_USING_GEOIP:
            return

        if not hasattr(self, '_geoip_data'):
            self._geoip_data = None
            try:
                gip = GeoIP(cache=GEOIP_CACHE_TYPE)
                self._geoip_data = gip.city(self.ip_address)
            except GeoIPException:
                msg = 'Error getting GeoIP data for IP "{0}"'.format(
                    self.ip_address)
                log.exception(msg)

        return self._geoip_data

    class Meta(object):
        ordering = ('-start_time',)
        permissions = (
            ('visitor_log', 'Can view visitor'),
        )


class Pageview(models.Model):
    visitor = models.ForeignKey(
        Visitor,
        related_name='pageviews',
        on_delete=models.CASCADE,
    )
    url = models.TextField(null=False, editable=False)
    referer = models.TextField(null=True, editable=False)
    query_string = models.TextField(null=True, editable=False)
    method = models.CharField(max_length=20, null=True)
    view_time = models.DateTimeField()
    summarized = models.BooleanField(default=False)

    objects = PageviewManager()

    class Meta(object):
        ordering = ('-view_time',)


class VisitSummary(models.Model):
    date = models.DateField()
    application_name = models.CharField(max_length=100, blank=True, null=True)
    page_visits = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(object):
        ordering = ('-date',)
        unique_together = [("date","application_name", "user"),]


class Email(models.Model):
    from_email = models.CharField(blank=True, null=True, editable=False, max_length=250)
    recipient_list = models.TextField(blank=True, null=True, editable=False)
    subject = models.CharField(blank=True, null=True, editable=False, max_length=1000)
    sent_at = models.DateTimeField(auto_now_add=True, editable=False)
    sent_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, editable=False, related_name='email_sent_by')
    send_method = models.CharField(blank=True, null=True, editable=False, max_length=100)
    msg_id = models.CharField(blank=True, null=True, editable=False, max_length=100)
