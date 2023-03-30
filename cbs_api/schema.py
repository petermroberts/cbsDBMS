import graphene
import Donors.schema
import Donations.schema
import Warehouses.schema

class Query(
    Donors.schema.Query, 
    Donations.schema.Query,
    Warehouses.schema.Query,
    graphene.ObjectType
    ):
    pass

class Mutation(
    Donors.schema.Mutation,
    Donations.schema.Mutation,
    Warehouses.schema.Mutation,
    graphene.ObjectType
    ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)