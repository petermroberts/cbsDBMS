from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Donor)
admin.site.register(ContactInfo)
admin.site.register(ShippingInfo)