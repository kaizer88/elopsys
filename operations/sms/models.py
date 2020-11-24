
import logging
import datetime
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict
logger = logging.getLogger(__name__)
from django.db import models

class SmsMessage(models.Model):
    content = models.CharField(_('Content'), max_length=350, blank=False)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=False)
    created = models.DateTimeField(blank=False, null=False)
    sent = models.NullBooleanField(_('Sent'), default=None, editable=False)
    last_attempt = models.DateTimeField(_('Last attempt'), auto_now=False, auto_now_add=False, blank=True, null=True, editable=False)
    error_msg = models.TextField(_('Last error'), null=True, blank=True)
    vehicle = models.ForeignKey("fleet.Vehicle", null=True, blank=True, related_name='vehicle_smses')
    driver = models.ForeignKey("employees.Employee", null=True, blank=True, related_name='driver_smses')


    def __unicode__(self):
        return self.content

    def model_to_dict(self):
        d = model_to_dict(self)
        d['sent'] = self.sent
        return d

# Create your models here.
