import graphene
import Donors.schema

class Query(
    Donors.schema.Query, 
    graphene.ObjectType
    ):
    pass

class Mutation(
    Donors.schema.Mutation,
    graphene.ObjectType
    ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)