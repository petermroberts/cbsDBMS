import graphene
import Donors.schema

class Query(Donors.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)