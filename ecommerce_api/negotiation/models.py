from django.db import models

from common.models import BaseModel
from users.models import Address

class Negotiation(BaseModel):

    TYPE_CHOICES = [
        (1, 'Venda'),
        (2, 'Troca'),
        (3, 'Desejo'),
    ]

    URGENCY_CHOICES = [
        (1, 'Baixa'),
        (2, 'Média'),
        (3, 'Alta'),
        (4, 'Data'),
    ]

    type: models.IntegerField(choices=TYPE_CHOICES)
    value = models.FloatField()
    description = models.CharField(max_length=255)
    trade_for = models.CharField(max_length=255)
    location = models.OneToOneField(Address, null=True, on_delete=models.SET_NULL)
    urgency = models.IntegerField(choices=URGENCY_CHOICES)
    limit_date = models.DateField()


class Picture(BaseModel):
    image: models.ImageField()
    negotiation: models.ForeignKey(Negotiation, on_delete=models.CASCADE)
