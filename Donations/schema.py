import graphene
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
    donation_by_id = graphene.Field(DonationType, id=graphene.ID(required=True))
    donations_by_blood_type = graphene.List(DonationType, blood_type=graphene.String(required=True))
    donations_by_donor = graphene.List(DonationType, donor_id=graphene.ID(required=True))
    donations_by_location = graphene.List(DonationType, warehouse_id=graphene.ID(required=True))
    donations_by_acceptance = graphene.List(DonationType, rejected=graphene.Boolean(required=True))

    all_blood_donations = graphene.List(BloodDonationType)
    blood_donations_by_blood_type = graphene.List(BloodDonationType, blood_type=graphene.String(required=True))
    blood_donations_by_location = graphene.List(BloodDonationType, warehouse_id=graphene.ID(required=True))

    all_plasma_donations = graphene.List(PlasmaDonationType)
    plasma_donations_by_blood_type = graphene.List(PlasmaDonationType, blood_type=graphene.String(required=True))
    plasma_donation_by_location = graphene.List(PlasmaDonationType, warehouse_id=graphene.ID(required=True))

    all_platelet_donations = graphene.List(PlateletDonationType)
    platelet_donations_by_blood_type = graphene.List(PlateletDonationType, blood_type=graphene.String(required=True))
    platelet_donation_by_location = graphene.List(PlateletDonationType, warehouse_id=graphene.ID(required=True))

    all_samples = graphene.List(SampleType)
    samples_by_id = graphene.Field(SampleType, id=graphene.ID(required=True))
    samples_by_infection = graphene.List(SampleType, infection=graphene.String(required=True))
    samples_by_donor = graphene.List(SampleType, donor_id=graphene.ID(required=True))

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
    
    def resolve_all_plasma_donations(self, info, **kwargs):
        return PlasmaDonation.objects.all()
    
    def resolve_plasma_donations_by_blood_type(self, info, blood_type):
        return PlasmaDonation.objects.filter(donation__donor__blood_type=blood_type)

    def resolve_plasma_donations_by_location(self, info, warehouse_id):
        return PlasmaDonation.objects.filter(location__pk=warehouse_id)

    def resolve_all_platelet_donations(self, info, **kwargs):
        return PlateletDonation.objects.all()
    
    def resolve_platelet_donations_by_blood_type(self, info, blood_type):
        return PlateletDonation.objects.filter(donation__donor__blood_type=blood_type)

    def resolve_platelet_donations_by_location(self, info, warehouse_id):
        return PlateletDonation.objects.filter(location__pk=warehouse_id)

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
    sample = graphene.Field(SampleType)

    def mutate(self, info, donation_data):
        donor = Donor.objects.get(pk=donation_data.donor)
        donation = Donation(
            donor=donor,
            located=donation_data.located
        )
        donation.save()

        sample = Sample(
            donation=donation,
            located=donation_data.located
        )
        sample.save()

        return CreateDonation(donation=donation)

class CreateBloodDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)

    blood_donation = graphene.Field(BloodDonationType)

    def mutate(self, info, donation_id):
        donation = Donation.objects.get(pk=donation_id)
        blood_donation = BloodDonation(
            donation=donation,
            located=donation.located
        )
        blood_donation.save()
        donation.donation_used = True
        donation.save()
        return CreateBloodDonation(blood_donation=blood_donation)

class CreatePlasmaDonation(Mutation):
    class Arguments:
        blood_type = graphene.String(required=True)
        located = graphene.ID(required=True)

    plasma_donation = graphene.Field(PlasmaDonationType)

    def mutate(self, info, blood_type, located):
        donations = Donation.objects.filter(
            blood_type=blood_type, 
            donation_used=False,
            located=located
        ).order_by('date_collected')[:3]

        if len(donations) != 3:
            raise ValidationError(f"There are not donations of blood type {blood_type} to create this product")
        
        plasma_donation = PlasmaDonation.objects.create(located=located)

        for donation in donations:
            PlasmaDonationDonations.objects.create(
                plasma_donation=plasma_donation,
                donation=donation
            )
            donation.donation_used=True
            donation.save()

        return CreatePlasmaDonation(plasma_donation=plasma_donation)

class CreatePlateletDonation(Mutation):
    class Arguments:
        blood_type = graphene.String(required=True)
        located = graphene.ID(required=True)

    platelet_donation = graphene.Field(PlateletDonationType)

    def mutate(self, info, blood_type, located):
        donations = Donation.objects.filter(
            blood_type=blood_type, 
            donation_used=False,
            located=located
        ).order_by('date_collected')[:3]

        if len(donations) != 3:
            raise ValidationError(f"There are not donations of blood type {blood_type} to create this product")
        
        platelet_donation = PlateletDonation.objects.create(located=located)

        for donation in donations:
            PlateletDonationDonations.objects.create(
                platelet_donation=platelet_donation,
                donation=donation
            )
            donation.donation_used=True
            donation.save()

        return CreatePlateletDonation(platelet_donation=platelet_donation)

class UpdateDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)
        rejected = graphene.Boolean(required=False)
        donation_used = graphene.Boolean(required=False)

    donation = graphene.Field(DonationType)

    def mutate(self, info, donation_id, rejected=None, donation_used=None):
        donation = Donation.objects.get(pk=donation_id)
        if rejected is not None:
            donation.rejected = rejected
        if donation_used is not None:
            donation.donation_used = donation_used
        donation.save()
        return UpdateDonation(donation=donation)

class UpdateBloodDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)
        located = graphene.ID(required=True)

    blood_donation = graphene.Field(BloodDonationType)

    def mutate(self, info, donation_id, located=None):
        blood_donation = BloodDonation.objects.get(pk=donation_id)
        if located is not None:
            blood_donation.located = located
        blood_donation.save()

        return UpdateBloodDonation(blood_donation=blood_donation)

class UpdatePlasmaDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)
        located = graphene.ID(required=True)

    plasma_donation = graphene.Field(PlasmaDonationType)

    def mutate(self, info, donation_id, located=None):
        plasma_donation = PlasmaDonation.objects.get(pk=donation_id)
        if located is not None:
            plasma_donation.located = located
        plasma_donation.save()

        return UpdatePlasmaDonation(plasma_donation=plasma_donation)

class UpdatePlateletDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)
        located = graphene.ID(required=True)

    platelet_donation = graphene.Field(PlateletDonationType)

    def mutate(self, info, donation_id, located=None):
        platelet_donation = PlateletDonation.objects.get(pk=donation_id)
        if located is not None:
            platelet_donation.located = located
        platelet_donation.save()

        return UpdatePlateletDonation(platelet_donation=platelet_donation)

class UpdateSample(Mutation):
    class Arguments:
        sample_id = graphene.ID(required=True)
        infection = graphene.String(required=False)

    sample = graphene.Field(SampleType)

    def mutate(self, info, sample_id, infection=None):
        sample = Sample.objects.get(pk=sample_id)
        if infection is not None:
            sample.infection = infection
        sample.save()

        return UpdateSample(sample=sample)

class DeleteBloodDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)

    delete_success = graphene.Boolean()

    def mutate(self, info, donation_id):
        BloodDonation.objects.filter(pk=donation_id).delete()
        return DeleteBloodDonation(delete_success=True)

class DeletePlasmaDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)

    delete_success = graphene.Boolean()

    def mutate(self, info, donation_id):
        PlasmaDonation.objects.filter(pk=donation_id).delete()
        return DeletePlasmaDonation(delete_success=True)

class DeletePlateletDonation(Mutation):
    class Arguments:
        donation_id = graphene.ID(required=True)

    delete_success = graphene.Boolean()

    def mutate(self, info, donation_id):
        PlateletDonation.objects.filter(pk=donation_id).delete()
        return DeletePlateletDonation(delete_success=True)

class DeleteSample(Mutation):
    class Arguments:
        sample_id = graphene.ID(required=True)

    delete_success = graphene.Boolean()

    def mutate(self, info, sample_id):
        Sample.objects.get(pk=sample_id)
        return DeleteSample(delete_success=True)

#todo make CREATE, UPDATE, and DELETE methods for all types
class Mutation(object):
    create_donation = CreateDonation.Field()
    create_blood_donation = CreateBloodDonation.Field()
    create_plasma_donation = CreatePlasmaDonation.Field()
    create_platelet_donation = CreatePlateletDonation.Field()

    update_donation = UpdateDonation.Field()
    update_blood_donation = UpdateBloodDonation.Field()
    update_plasma_donation = UpdatePlasmaDonation.Field()
    update_platelet_donation = UpdatePlateletDonation.Field()
    update_sample = UpdateSample.Field()

    delete_blood_donation = DeleteBloodDonation.Field()
    delete_plasma_donation = DeletePlasmaDonation.Field()
    delete_platelet_donation = DeletePlateletDonation.Field()
    delete_sample = DeleteSample.Field()

    delete_expired_blood = graphene.Boolean()
    delete_expired_plasma = graphene.Boolean()
    delete_expired_platelets = graphene.Boolean()

def destroy_expired_donations():
    donation_expired()
    delete_expired_blood()
    delete_expired_plasma()
    delete_expired_platelets()

def donation_expired(self, info):
    donations = Donation.objects.all()
    expired_donation = [donation for donation in donations if is_donation_expired(donation)]
    for donation in expired_donation:
        donation.donation_used = True
        donation.save()
    return True

def delete_expired_blood(self, info):
    donations = BloodDonation.objects.all()
    expired_blood = [donation for donation in donations if is_blood_expired(donation)]
    for donation in expired_blood:
        donation.delete()
    return True

def delete_expired_plasma(self, info):
    donations = PlasmaDonation.objects.all()
    expired_plasma = [donation for donation in donations if is_plasma_expired(donation)]
    for donation in expired_plasma:
        donation.delete()
    return True

def delete_expired_platelets(self, info):
    donations = PlateletDonation.objects.all()
    expired_platelets = [donation for donation in donations if is_platelets_expired(donation)]
    for donation in expired_platelets:
        donation.delete()
    return True

def is_donation_expired(donation):
    days_since_donation = (date.today() - donation.date_collected).days
    return days_since_donation >= 35

def is_blood_expired(donation):
    days_since_donation = (date.today() - donation.date_collected).days
    return days_since_donation >= 42

def is_plasma_expired(donation):
    days_since_donation = (date.today() - donation.date_collected).days
    return days_since_donation >= 365

def is_platelets_expired(donation):
    days_since_donation = (date.today() - donation.date_collected).days
    return days_since_donation >= 5