from common.models import BaseModel
from delivery.models import Address
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Product(BaseModel):
    description = models.CharField(max_length=255)
    weight = models.FloatField(validators=[MaxValueValidator(50)])
    length = models.FloatField(validators=[MinValueValidator(15), MaxValueValidator(100)])
    height = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    width = models.FloatField(validators=[MinValueValidator(10), MaxValueValidator(100)])
    diameter = models.FloatField(default=0, validators=[MaxValueValidator(100)])

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if sum([self.length, self.height, self.width]) > 200:
            raise ValidationError(
                {'size': "The sum of the length, height, and width can't be bigger than 200cm."}
            )


class Picture(BaseModel):
    image = models.ImageField(upload_to='pictures')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')


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

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    type = models.IntegerField(choices=TYPE_CHOICES)
    value = models.FloatField()
    trade_for = models.CharField(max_length=255)
    location = models.OneToOneField(Address, on_delete=models.PROTECT)
    urgency = models.IntegerField(choices=URGENCY_CHOICES)
    limit_date = models.DateField()


class Bid(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    deal = models.ForeignKey(Deal, on_delete=models.PROTECT)
    accepted = models.BooleanField(default=False)
    value = models.FloatField()
    description = models.CharField(max_length=255)


class Message(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    deal = models.ForeignKey(Deal, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)


class Payment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    deal = models.OneToOneField(Deal, on_delete=models.PROTECT)
