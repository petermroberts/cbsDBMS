from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Donation)
admin.site.register(BloodDonation)
admin.site.register(PlasmaDonation)
admin.site.register(PlateletDonation)

admin.site.register(Sample)
