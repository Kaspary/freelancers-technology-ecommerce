import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from common.models import BaseModel


class RequestPasswordToken(BaseModel):
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{} - {}'.format(self.user.email, self.token)


class ConfirmEmailToken(BaseModel):
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{} - {}'.format(self.user.email, self.token)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    token = Token.objects.filter(user=instance)
    if instance.is_staff and not token.exists():
        Token.objects.create(user=instance)
    elif not instance.is_staff and token.exists():
        token.delete()
