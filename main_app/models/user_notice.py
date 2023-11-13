import uuid
from django.db import models
from django.utils import timezone
from .user import User

class UserNotice(models.Model):
    id       = models.UUIDField(primary_key=True, editable=False, blank=False, null=False, default=uuid.uuid4)
    datetime = models.DateTimeField(blank=False, null=False, default=timezone.now)
    user     = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False, related_name="user")
    title    = models.CharField(max_length=100, blank=False, null=False, default="No Title")
    message  = models.TextField(blank=False, null=False, default="No Message")
    url      = models.URLField(blank=True, null=True)
