from django.db import models
from django.db.models import CheckConstraint, Q

# Create your models here.
class Warehouse(models.Model):
    pass

class WarehouseShippingInfo(models.Model):
    PROVINCE_ALBERTA = 'AB'
    PROVINCE_BRITISHCOLUMBIA = 'BC'
    PROVINCE_MANITOBA = 'MB'
    PROVINCE_NEWBRUNSWICK = 'NB'
    PROVINCE_NEWFOUNDLANDLABRADOR = 'NL'
    PROVINCE_NORTHWESTTERRITORIES = 'NT'
    PROVINCE_NOVASCOTIA = 'NS'
    PROVINCE_NUNAVUT = 'NU'
    PROVINCE_ONTARIO = 'ON'
    PROVINCE_PEI = 'PE'
    PROVINCE_QUEBEC = 'QC'
    PROVINCE_SASKATCHEWAN = 'SK'
    PROVINCE_YUKON = 'YT'

    PROVINCE_CHOICES = [
        (PROVINCE_ALBERTA, 'Alberta'),
        (PROVINCE_BRITISHCOLUMBIA, 'British Columbia'),
        (PROVINCE_MANITOBA, 'Manitoba'),
        (PROVINCE_NEWBRUNSWICK, 'New Brunswick'),
        (PROVINCE_NEWFOUNDLANDLABRADOR, 'Newfoundland and Labrador'),
        (PROVINCE_NORTHWESTTERRITORIES, 'Norhtwest Territories'),
        (PROVINCE_NOVASCOTIA, 'Nova Scotia'),
        (PROVINCE_NUNAVUT, 'Nunavut'),
        (PROVINCE_ONTARIO, 'Ontario'),
        (PROVINCE_PEI, 'Prince Edward Island'),
        (PROVINCE_QUEBEC, 'Quebec'),
        (PROVINCE_SASKATCHEWAN, 'Saskatchewan'),
        (PROVINCE_YUKON, 'Yukon'),
    ]

    warehouse = models.OneToOneField(Warehouse, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=7)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(province__in=('AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT')), name='warehouse_province_invalid'
            )
        ]