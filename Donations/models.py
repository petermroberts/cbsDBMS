# from django.db import models
# from Donors.models import *
# from Warehouses.models import *

# # Create your models here.

# class Donation(models.Model):
#     donation_id = models.AutoField(primary_key=True)
#     date_collected = models.DateField(auto_now_add=True)
#     rejected = models.BooleanField(default=False)
#     donor = models.ForeignKey(Donor, on_delete=models.PROTECT)
#     located = models.OneToOneField(Warehouse, on_delete=models.CASCADE, default=None)