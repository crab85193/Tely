import uuid
from django.db import models
from django.utils import timezone

class Twilio(models.Model):
    id                    = models.UUIDField(primary_key=True, editable=False, blank=False, null=False, default=uuid.uuid4)
    account_sid           = models.CharField(max_length=1000, blank=False, null=False) 
    record_datetime       = models.DateTimeField(blank=False, null=False, default=timezone.now)
    name                  = models.CharField(max_length=1000, blank=False, null=False)
    type                  = models.CharField(max_length=1000, blank=False, null=False)
    open                  = models.CharField(max_length=1000, blank=False, null=False)
    photo_url             = models.URLField(max_length=1000, blank=False, null=False)
    rating                = models.CharField(max_length=10, blank=True, null=True)
    price_level           = models.CharField(max_length=10, blank=True, null=True)
    archive               = models.BooleanField(blank=False, null=False, default=False)
    recommend             = models.BooleanField(blank=False, null=False, default=True)
    number_of_reservation = models.PositiveIntegerField(blank=False, null=False, default=0)