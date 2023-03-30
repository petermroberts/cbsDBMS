from django.db import models
from Donors.models import *
from Warehouses.models import *

# Create your models here.

class Donation(models.Model):
    date_collected = models.DateField(auto_now_add=True)
    rejected = models.BooleanField(default=False)
    donor = models.ForeignKey(Donor, on_delete=models.PROTECT)
    located = models.OneToOneField(Warehouse, on_delete=models.CASCADE, blank=True, null=True)
    donation_used = models.BooleanField(default=False)

# hello
class BloodDonation(models.Model):
    #! donations shouldn't be allowed to be deleted, but if one is with a product.. keep the product
    donation = models.OneToOneField(Donation, on_delete=models.PROTECT)
    located = models.OneToOneField(Warehouse, on_delete=models.CASCADE)

class PlasmaDonationDonations(models.Model):
    plasma_donation = models.ForeignKey('PlasmaDonation', on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.PROTECT)

class PlasmaDonation(models.Model):
    donations = models.ManyToManyField(Donation, through='PlasmaDonationDonations')

class PlateletDonationDonations(models.Model):
    platelet_donation = models.ForeignKey('PlateletDonation', on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.PROTECT)

class PlateletDonation(models.Model):
    donations = models.ManyToManyField(Donation, through='PlateletDonationDonations')

class Sample(models.Model):
    INFECTION_CHOICES = [
        ('Syphilis', 'Syphilis'),
        ('HEP_B', 'Hepatitis B'),
        ('HEP_C', 'Hepatitis C'),
        ('HIV_1', 'Human Immunodeficiency Virus 1'),
        ('HIV_2', 'Human Immunodeficiency Virus 2'),
        ('HTLV_1', 'Human T-Lymphotropic Virus 1'),
        ('HTLV_2', 'Human T-Lymphotropic Virus 2'),
        ('WNV', 'West Nile Virus'),
        ('CMV', 'Cytomegalovirus'),
        ('CD', 'Chagas Disease  '),
    ]
    donation = models.ForeignKey(Donation, on_delete=models.PROTECT)
    infection = models.CharField(max_length=127, choices=INFECTION_CHOICES, default=None, blank=True, null=True)
    located = models.OneToOneField(Warehouse, on_delete=models.CASCADE)

# #todo review these two models
# class Order(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
    
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     donation = models.ForeignKey(Donation, on_delete=models.PROTECT)
#     product = models.TextChoices('Product', 'BLOOD PLASMA PLATELETS')