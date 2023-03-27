import graphene
from graphene import Mutation
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from .models import *
from .forms import *


class DonorType(DjangoObjectType):
    class Meta:
        model = Donor
        fields = '__all__'

#* donor POST method
class CreateDonor(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        date_of_birth = graphene.Date(required=True)
        blood_type = graphene.String(required=True)

    donor = graphene.Field(DonorType)

    def mutate(self, info, first_name, last_name, date_of_birth, blood_type):
        donor = Donor.objects.create(
            first_name=first_name, 
            last_name=last_name, 
            date_of_birth=date_of_birth,
            blood_type=blood_type)
        return CreateDonor(donor=donor)

#* donor UPDATE method
class UpdateDonor(graphene.Mutation):
    class Arguments:
        donor_id = graphene.BigInt(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    donor = graphene.Field(DonorType)

    def mutate(self, info, donor_id, first_name=None, last_name=None):
        donor = Donor.objects.get(pk=donor_id)
        if first_name is not None:
            donor.first_name = first_name
        if last_name is not None:
            donor.last_name = last_name
        donor.save()
        return UpdateDonor(donor=donor)

#* donor DELETE method
class DeleteDonor(graphene.Mutation):
    class Arguments:
        donor_id = graphene.BigInt(required=True)

    delete_success = graphene.Boolean()

    def mutate(self, info, donor_id):
        Donor.objects.filter(pk=donor_id).delete()
        return DeleteDonor(delete_success=True)    

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
    
class Mutation(object):
    create_donor = CreateDonor.Field()
    update_donor = UpdateDonor.Field()
    delete_donor = DeleteDonor.Field()