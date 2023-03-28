import graphene
import Donors.schema
import Donations.schema

class Query(
    Donors.schema.Query, 
    Donations.schema.Query,
    graphene.ObjectType
    ):
    pass

class Mutation(
    Donors.schema.Mutation,
    Donations.schema.Mutation,
    graphene.ObjectType
    ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)