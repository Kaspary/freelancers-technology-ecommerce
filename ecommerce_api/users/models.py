from common.models import BaseModel
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from delivery.models import Address


class User(AbstractUser):
    location = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, related_name='user')

    @property
    def is_manager(self):
        return self.is_superuser or self.is_staff


class Invite(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sended_invites')
    user_invited = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='invites')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    token = Token.objects.filter(user=instance)
    if instance.is_staff and not token.exists():
        Token.objects.create(user=instance)
    elif not instance.is_staff and token.exists():
        token.delete()
