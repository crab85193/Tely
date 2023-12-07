import uuid
from django.db import models
from django.utils import timezone
from .user import User

class Notice(models.Model):
    WARNING = 0
    DANGER  = 1
    SUCCESS = 2
    PRIMARY = 3

    NOTICETYPE = (
        (WARNING, 'Warning'),
        (DANGER , 'Danger' ),
        (SUCCESS, 'Success'),
        (PRIMARY, 'Primary'),
    )

    id       = models.UUIDField(primary_key=True, editable=False, blank=False, null=False, default=uuid.uuid4)
    datetime = models.DateTimeField(blank=False, null=False, default=timezone.now)
    title    = models.CharField(max_length=100, blank=False, null=False, default="No Title")
    message  = models.TextField(blank=False, null=False, default="No Message")
    type     = models.IntegerField(blank=False, null=False, default=0, choices=NOTICETYPE)
    url      = models.URLField(blank=True, null=True)
    archive  = models.BooleanField(blank=False, null=False, default=False)


class UserNotice(models.Model):
    WARNING = 0
    DANGER  = 1
    SUCCESS = 2
    PRIMARY = 3

    NOTICETYPE = (
        (WARNING, 'Warning'),
        (DANGER , 'Danger' ),
        (SUCCESS, 'Success'),
        (PRIMARY, 'Primary'),
    )

    id       = models.UUIDField(primary_key=True, editable=False, blank=False, null=False, default=uuid.uuid4)
    datetime = models.DateTimeField(blank=False, null=False, default=timezone.now)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="notice_user")
    title    = models.CharField(max_length=100, blank=False, null=False, default="No Title")
    message  = models.TextField(blank=False, null=False, default="No Message")
    type     = models.IntegerField(blank=False, null=False, default=0, choices=NOTICETYPE)
    url      = models.URLField(blank=True, null=True)
    is_check = models.BooleanField(blank=False, null=False, default=False)
