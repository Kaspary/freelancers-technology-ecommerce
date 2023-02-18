from django.core.validators import RegexValidator
from django.db import models
from common.models import BaseModel


class Address(BaseModel):
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=8, validators=[
        RegexValidator(regex='^\d\d\d\d\d\d\d\d$',message='Zip Code must be just number, with 8 digits')
    ])
