from django.db import models

# Create your models here.
class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)