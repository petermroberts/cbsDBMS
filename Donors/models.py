from django.db import models
from django.db.models import CheckConstraint, Q, F
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

    donor_id = models.AutoField(primary_key=True)
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

class DonorForm(ModelForm):
    class Meta:
        model = Donor
        fields = '__all__'


class ContactInfo(models.Model):
    donor = models.OneToOneField(
        Donor,
        on_delete=models.CASCADE,
        primary_key=True
    )
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)

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
    
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE, primary_key=True)
    postal_code = models.CharField(max_length=7)
    civic_number = models.PositiveSmallIntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(province__in=('AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT')), name='province_invalid'
            ),
            CheckConstraint(
            check=Q(civic_number__gt=0), name='civic_number_invalid'
            )
        ]