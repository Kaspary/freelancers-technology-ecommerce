from django.conf import settings
from django.db import models

from common.models import BaseModel
from delivery.models import Address

class Deal(BaseModel):

    TYPE_CHOICES = [
        (1, 'Venda'),
        (2, 'Troca'),
        (3, 'Desejo'),
    ]

    URGENCY_CHOICES = [
        (1, 'Baixa'),
        (2, 'Média'),
        (2, 'Média'),
        (3, 'Alta'),
        (4, 'Data'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    value = models.FloatField()
    description = models.CharField(max_length=255)
    trade_for = models.CharField(max_length=255)
    location = models.OneToOneField(Address, null=True, on_delete=models.SET_NULL)
    urgency = models.IntegerField(choices=URGENCY_CHOICES)
    limit_date = models.DateField()


class Picture(BaseModel):
    image = models.ImageField(upload_to='pictures')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='pictures')


class Bid(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    value = models.FloatField()
    description = models.CharField(max_length=255)


class Message(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)