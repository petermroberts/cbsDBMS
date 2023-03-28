import graphene, json
from graphene import InputObjectType, Mutation
from graphene_django import DjangoObjectType
from .models import *
from datetime import date

class DonationType(DjangoObjectType):
    class Meta:
        model = Donation
        fields = '__all__'

class BloodDonationType(DjangoObjectType):
    class Meta:
        model = BloodDonation

class PlasmaDonationDonationsType(DjangoObjectType):
    class Meta:
        model = PlasmaDonationDonations

class PlasmaDonationType(DjangoObjectType):
    class Meta:
        model = PlasmaDonation

class PlateletDonationDonationsType(DjangoObjectType):
    class Meta:
        model = PlateletDonationDonations
    
class PlateletDonationType(DjangoObjectType):
    class Meta:
        model = PlateletDonation

class SampleType(DjangoObjectType):
    class Meta:
        model = Sample

#todo make queries for plasma and platelet donations
class Query(object):
    all_donations = graphene.List(DonationType)
    donation_by_id = graphene.Field(DonationType, id=graphene.ID())
    donations_by_blood_type = graphene.List(DonationType, blood_type=graphene.String())
    donations_by_donor = graphene.List(DonationType, donor_id=graphene.ID(required=True))
    donations_by_location = graphene.List(DonationType, warehouse_id=graphene.ID(required=True))
    donations_by_acceptance = graphene.List(DonationType, rejected=graphene.Boolean())

    all_blood_donations = graphene.List(BloodDonationType)
    blood_donations_by_blood_type = graphene.List(BloodDonationType, blood_type=graphene.String(required=True))
    blood_donations_by_location = graphene.List(BloodDonationType, warehouse_id=graphene.ID())

    all_samples = graphene.List(SampleType)
    samples_by_id = graphene.Field(SampleType, id=graphene.ID())
    samples_by_infection = graphene.List(SampleType, infection=graphene.String(required=True))
    samples_by_donor = graphene.List(SampleType, donor_id=graphene.ID())

    def resolve_all_donations(self, info, **kwargs):
        return Donation.objects.all()
    
    def resolve_donation_by_id(self, info, id):
        return Donation.objects.get(pk=id)

    def resolve_donations_by_blood_type(self, info, blood_type):
        return Donation.objects.filter(donor__blood_type=blood_type)
        
    def resolve_donations_by_donor(self, info, donor_id):
        return Donation.objects.filter(donor__pk=donor_id)
    
    def resolve_donations_by_location(self, info, warehouse_id):
        return Donation.objects.filter(location__pk=warehouse_id)
    
    def resolve_donations_by_acceptance(self, info, rejected):
        return Donation.objects.filter(rejected=rejected)
    
    def resolve_all_blood_donations(self, info, **kwargs):
        return BloodDonation.objects.all()
    
    def resolve_blood_donations_by_blood_type(self, info, blood_type):
        return BloodDonation.objects.filter(donation__donor__blood_type=blood_type)
    
    def resolve_blood_donations_by_location(self, info, warehouse_id):
        return BloodDonation.objects.filter(location__pk=warehouse_id)

    def resolve_all_samples(self, info, **kwargs):
        return Sample.objects.all()
    
    def resolve_samples_by_id(self, info, id):
        return Sample.objects.get(pk=id)
    
    def resolve_samples_by_infection(self, info, infection):
        return Sample.objects.filter(infection=infection)
    
    def resolve_samples_by_donor(self, info, donor_id):
        return Sample.objects.filter(donation__donor__pk=donor_id)

class CreateDonationInput(InputObjectType):
    donor = graphene.ID(required=True)
    located = graphene.ID(required=False)

class CreateDonation(Mutation):
    class Arguments:
        donation_data = CreateDonationInput(required=True)

    donation = graphene.Field(DonationType)

    def mutate(self, info, donation_data):
        donor = Donor.objects.get(pk=donation_data.donor)
        donation = Donation(
            donor=donor,
            located=donation_data.located
        )
        donation.save()

        return CreateDonation(donation=donation)
    
class Mutation(object):
    create_donation = CreateDonation.Field()