from django_filters import rest_framework as filters

class DeliveryFilter(filters.FilterSet):
    service_options =[
        ('Sedex Varejo', 40010),
        ('Sedex A Cobrar Varejo', 40045),
        ('Sedex 10 Varejo', 40215),
        ('Sedex Hoje Varejo', 40290),
        ('Pac Varejo', 41106)
    ]
    service = filters.ChoiceFilter(choices=service_options)
