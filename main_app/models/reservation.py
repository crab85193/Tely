import uuid
from django.db import models
from django.utils import timezone
from .user import User
from django.utils.translation import gettext_lazy as _

class ReservationParent(models.Model):
    id                   = models.UUIDField(primary_key=True, editable=False, blank=False, null=False, default=uuid.uuid4)
    user                 = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="reservate_user")
    sid                  = models.CharField(blank=True, null=True, max_length=34, default="")
    shop_tel_number      = models.CharField(blank=False, null=False, max_length=15)
    shop_name            = models.CharField(blank=False, null=False, max_length=100, verbose_name=_("Store Name"))
    reservation_datetime = models.DateTimeField(blank=False, null=False, verbose_name=_("Reservation Time"))
    num_people           = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name=_("Number of Reserved People"))
    representative_name  = models.CharField(blank=False, null=False, max_length=100, verbose_name=_("Name of Representative"))
    memo                 = models.TextField(blank=True, null=True, verbose_name=_("Memo"))
    start_datetime       = models.DateTimeField(blank=False, null=False, default=timezone.now)
    end_datetime         = models.DateTimeField(blank=True, null=True)
    is_end               = models.BooleanField(blank=False, null=False, default=False)
    place_id             = models.CharField(blank=True, null=True, max_length=1000)
    

class ReservationChild(models.Model):
    NOSTATE = 0
    START   = 1
    FAILURE = 2
    SUCCESS = 3
    WAIT    = 4
    CANCEL  = 5
    END     = 6
    SYSTEM  = 7
    ERROR   = 8
    UNKNOWN = 9

    CHILDSTATUS = (
        (NOSTATE, 'NoState'),
        (START,   'Start'  ),
        (FAILURE, 'Failure'),
        (SUCCESS, 'Success'),
        (WAIT   , 'Wait'   ),
        (CANCEL , 'Cancel' ),
        (END    , 'End'    ),
        (SYSTEM , 'System' ),
        (ERROR  , 'Error'  ),
        (UNKNOWN, 'Unknown'),
    )

    id         = models.UUIDField(primary_key=True, editable=False, blank=False, null=False, default=uuid.uuid4)
    parent     = models.ForeignKey(ReservationParent, on_delete=models.CASCADE, blank=False, null=False, related_name="reservation_parent")
    datetime   = models.DateTimeField(blank=False, null=False, default=timezone.now)
    status     = models.IntegerField(blank=False, null=False, default=0, choices=CHILDSTATUS)
    title_ja   = models.CharField(max_length=100, blank=False, null=False, default="No Title")
    title_en   = models.CharField(max_length=100, blank=False, null=False, default="No Title")
    message_ja = models.TextField(blank=False, null=False, default="No Message")
    message_en = models.TextField(blank=False, null=False, default="No Message")
