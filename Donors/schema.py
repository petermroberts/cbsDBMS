import graphene
from graphene import InputObjectType, Mutation
from graphene_django import DjangoObjectType
from .models import *
from .forms import *


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

class DonorContactInfoType(DjangoObjectType):
    class Meta:
        model = DonorContactInfo

class DonorShippingInfoType(DjangoObjectType):
    class Meta:
        model = DonorShippingInfo

class Query(object):
    all_donors = graphene.List(DonorType)
    donors_by_blood_type = graphene.Field(DonorType, blood_type=graphene.String())
    donors_by_id = graphene.Field(DonorType, id=graphene.ID())

    contact_info_by_donor = graphene.Field(ContactInfoType, id=graphene.ID())
    shipping_by_donor = graphene.Field(ShippingInfoType, id=graphene.ID())

    def resolve_all_donors(root, info, **kwargs):
        return Donor.objects.all()
    
    def resolve_donors_by_blood_type(root, info, blood_type):
        return Donor.objects.get(blood_type=blood_type)
    
    def resolve_donors_by_id(root, info, id):
        return Donor.objects.get(pk=id)
    
    def resolve_contact_info_by_donor(root, info, id):
        return ContactInfo.objects.get(donorcontactinfo__pk=id)
    
    def resolve_shipping_by_donor(root, info, id):
        return ShippingInfo.objects.get(donorshippinginfo__pk=id)
    
#? These three classes hold the arguments for creating the three models in this app
class CreateContactInfoInput(InputObjectType):
    phone = graphene.String(required=False)
    email = graphene.String(required=False)

class CreateShippingInfoInput(InputObjectType):
    postal_code = graphene.String(required=True)
    address = graphene.String(required=True)
    city = graphene.String(required=True)
    province = graphene.String(required=True)

class CreateDonorInput(InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    date_of_birth = graphene.Date(required=True)
    blood_type = graphene.String(required=True)
    contact_info = CreateContactInfoInput(required=True)
    shipping_info = CreateShippingInfoInput(required=True)

#* donor POST method, This will also create contact and shipping info
class CreateDonor(Mutation):
    class Arguments:
        donor_data = CreateDonorInput(required=True)

    donor = graphene.Field(DonorType)

    def mutate(self, info, donor_data):
        # Create ContactInfo object type and save it to the db
        contact_info = ContactInfo(
            phone=donor_data.contact_info.phone,
            email=donor_data.contact_info.email
        )
        contact_info.save()

        # Create teh DonorContactInfo relation and save it to the db
        donor_contact_info = DonorContactInfo(
            donor = None,
            contact_info = contact_info
        )
        donor_contact_info.save()

        # Create the ShippingInfo object and save it to db
        shipping_info = ShippingInfo(
            postal_code=donor_data.shipping_info.postal_code,
            address=donor_data.shipping_info.address,
            city=donor_data.shipping_info.city,
            province=donor_data.shipping_info.province
        )
        shipping_info.save()

        # Create the DonorShippingInfo relation and save it to the db
        donor_shipping_info = DonorShippingInfo(
            donor=None,
            shipping_info=shipping_info
        )
        donor_shipping_info.save()
        
        # Create the Donor object and save it to the db along with the contact and shipping info
        donor = Donor(
            first_name=donor_data.first_name,
            last_name=donor_data.last_name,
            date_of_birth=donor_data.date_of_birth,
            blood_type=donor_data.blood_type,
            contact_info=contact_info,
            shipping_info=shipping_info
        )
        donor.save()

        # Save the create donors id as the id for the two relations
        donor_contact_info.donor = donor
        donor_contact_info.save()
        donor_shipping_info.donor = donor
        donor_shipping_info.save()

        return CreateDonor(donor=donor)

#* donor UPDATE method
class UpdateDonor(Mutation):
    class Arguments:
        donor_id = graphene.BigInt(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    donor = graphene.Field(DonorType)

    # Update donor entity if at least one of the two attributes below are modified
    #* Note that date_of_birth and blood_type won't be modified
    def mutate(self, info, donor_id, first_name=None, last_name=None):
        donor = Donor.objects.get(pk=donor_id)
        if first_name is not None:
            donor.first_name = first_name
        if last_name is not None:
            donor.last_name = last_name
        donor.save() # save the modifications
        return UpdateDonor(donor=donor)

#* donor DELETE method
class DeleteDonor(Mutation):
    class Arguments:
        donor_id = graphene.BigInt(required=True)

    delete_success = graphene.Boolean() # verify that the entity was deleted

    def mutate(self, info, donor_id):
        Donor.objects.filter(pk=donor_id).delete()
        return DeleteDonor(delete_success=True)
    
class CreateContactInfo(Mutation):
    class Arguments:
        donor_id = graphene.ID(required=True) # need the id of the donor we want to add contact info to
        contact_data = CreateContactInfoInput(required=True)
    
    contact_info = graphene.Field(ContactInfoType)

    #* Like CreateDonor but only need to create a ContactInfo entity and ConorContactInfo relation
    def mutate(self, info, donor_id, contact_data):
        donor = Donor.objects.get(pk=donor_id)
        contact_info = ContactInfo(
            phone=contact_data.phone,
            email=contact_data.email
        )
        contact_info.save()

        donor_contact_info = DonorContactInfo(
            donor=donor, #* because we are explicitly given an id we can set it right away
            contact_info=contact_info
        )
        donor_contact_info.save()

class UpdateContactInfo(Mutation):
    class Arguments:
        contact_info_id = graphene.ID(required=True)
        contact_data = CreateContactInfoInput(required=True)

    contact_info = graphene.Field(ContactInfoType)

    def mutate(self, info, contact_info_id, contact_data):
        contact_info = ContactInfo.objects.get(pk=contact_info_id)
        if contact_data.phone is not None:
            contact_info.phone = contact_data.phone
        if contact_data.email is not None:
            contact_info.email = contact_data.email
        contact_info.save()
        return UpdateContactInfo(contact_info=contact_info)

class Mutation(object):
    create_donor = CreateDonor.Field()
    update_donor = UpdateDonor.Field()
    delete_donor = DeleteDonor.Field()