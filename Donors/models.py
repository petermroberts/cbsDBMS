from django.db import models
from django.db.models import CheckConstraint, Q
from django.core.exceptions import ValidationError
from django.forms import ModelForm

# Create your models here.
class Donor(models.Model):
    BLOODTYPE_CHOICES = [
        ('AP', "A+"),
        ('AN', "A-"),
        ('BP', "B+"),
        ('BN', "B-"),
        ('ABP', "AB+"),
        ('ABN', "AB-"),
        ('OP', "O+"),
        ('ON', "O-"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=3, choices=BLOODTYPE_CHOICES)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(blood_type__in=('AP', 'AN', 'BP', 'BN', 'ABP', 'ABN', 'OP', 'ON')), name='blood_type'
            )
        ]
    
    def clean(self):
        if self.blood_type not in ['AP', 'AN', 'BP', 'BN', 'ABP', 'ABN', 'OP', 'ON']:
            raise ValidationError({'blood_type': "Invalid Blood Type"})

class DonorContactInfo(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    contact_info = models.ForeignKey('ContactInfo', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('donor', 'contact_info'))

class ContactInfo(models.Model):
    donor = models.ManyToManyField(
        Donor,
        through=DonorContactInfo,
        blank=True,
        related_name='contact_info',
        # on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)

class DonorShippingInfo(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    shipping_info = models.ForeignKey('ShippingInfo', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('donor', 'shipping_info'),)

class ShippingInfo(models.Model):
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
    
    donors = models.ManyToManyField(
        Donor, 
        through=DonorShippingInfo, 
        blank=True,
        related_name='shipping_info', 
        # on_delete=models.CASCADE
        )
    postal_code = models.CharField(max_length=7)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(province__in=('AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT')), name='province_invalid'
            )
        ]