import uuid
from datetime import datetime
from django.db import models
from django.conf import settings

class UserActivateTokensManager(models.Manager):
    def activate_user_by_token(self, activate_token):
        user_activate_token = self.filter(
            activate_token=activate_token,
            expired_at__gte=datetime.now()
        ).first()
        if hasattr(user_activate_token, 'user'):
            user = user_activate_token.user
            user.is_active = True
            user.save()
            return user
    
    def get_or_none(self, **kwargs):
       try:
           return self.get_queryset().get(**kwargs)
       except self.model.DoesNotExist:
           return None


class UserActivateTokens(models.Model):
    token_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activate_token = models.UUIDField(default=uuid.uuid4)
    expired_at = models.DateTimeField()

    objects = UserActivateTokensManager()
        