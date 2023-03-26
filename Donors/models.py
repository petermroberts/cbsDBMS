from django.db import models

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