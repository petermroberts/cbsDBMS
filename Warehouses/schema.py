import graphene
from graphene import InputObjectType, Mutation
from graphene_django import DjangoObjectType
from .models import *

class WarehouseType(DjangoObjectType):
    class Meta:
        model = Warehouse

class WarehouseShippingInfoType(DjangoObjectType):
    class Meta:
        model = WarehouseShippingInfo

class Query(object):
    all_warehouses = graphene.List(WarehouseType)
    warehouse_by_id = graphene.List(WarehouseType, id=graphene.ID(require=True))
    warehouses_by_province = graphene.List(WarehouseType, province=graphene.String(required=True))

    def resolve_all_warehouses(self, info, **kwargs):
        return Warehouse.objects.all()
    
    def resolve_warehouse_by_id(self, info, id):
        return Warehouse.objects.get(pk=id)
    
    def resolve_warehouses_by_province(self, info, province):
        return Warehouse.objects.filter(province=province)
