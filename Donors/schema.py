import graphene
from graphene_django import DjangoObjectType
from .models import *

class DonorType(DjangoObjectType):
    class Meta:
        model = Donor
        fields = '__all__'

class ContactInfoType(DjangoObjectType):
    class Meta:
        model = ContactInfo

class ShippingInfoType(DjangoObjectType):
    class Meta:
        model = ShippingInfo

class Query(object):
    all_donors = graphene.List(DonorType)
    donors_by_blood_type = graphene.Field(DonorType, blood_type=graphene.String())
    donors_by_id = graphene.Field(DonorType, donor_id=graphene.String())

    contact_info_by_donor = graphene.Field(ContactInfoType, donor_id=graphene.String())
    shipping_by_donor = graphene.Field(ShippingInfoType, donor_id=graphene.String())

    def resolve_all_donors(root, info, **kwargs):
        return Donor.objects.all()
    
    def resolve_donors_by_blood_type(root, info, blood_type):
        return Donor.objects.get(blood_type=blood_type)
    
    def resolve_donors_by_id(root, info, donor_id):
        return Donor.objects.get(pk=donor_id)
    
    def resolve_contact_info_by_donor(root, info, donor_id):
        return ContactInfo.objects.get(pk=donor_id)
    
    def resolve_shipping_by_donor(root, info, donor_id):
        return ShippingInfo.objects.get(pk=donor_id)