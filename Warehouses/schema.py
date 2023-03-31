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
    warehouse_by_id = graphene.List(WarehouseType, id=graphene.ID(required=True))
    warehouses_by_province = graphene.List(WarehouseType, province=graphene.String(required=True))

    def resolve_all_warehouses(self, info, **kwargs):
        return Warehouse.objects.all()
    
    def resolve_warehouse_by_id(self, info, id):
        return Warehouse.objects.get(pk=id)
    
    def resolve_warehouses_by_province(self, info, province):
        return Warehouse.objects.filter(province=province)

class CreateWarehouseShippingInfoInput(InputObjectType):
    postal_code = graphene.String(required=True)
    address = graphene.String(required=True)
    city = graphene.String(required=True)
    province = graphene.String(required=True)

class UpdateWarehouseShippingInfoInput(InputObjectType):
    postal_code = graphene.String(required=False)
    address = graphene.String(required=False)
    city = graphene.String(required=False)
    province = graphene.String(required=False)

class CreateWarehouse(Mutation):
    class Arguments:
        pass
        # shipping_data = CreateWarehouseShippingInfoInput(required=True)

    warehouse = graphene.Field(WarehouseType)

    def mutate(self, info, shipping_data):
        warehouse = Warehouse()
        warehouse.save()

        return CreateWarehouse(warehouse=warehouse)

class CreateWarehouseShippingInfo(Mutation):
    class Arguments:
        warehouse_id = graphene.ID(required=True)
        shipping_data = CreateWarehouseShippingInfoInput(required=True)

    warehouse_shipping_info = graphene.Field(WarehouseShippingInfoType)

    def mutate(self, info, warehouse_id, shipping_data):
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        warehouse_shipping_info = WarehouseShippingInfo(
            warehouse=warehouse,
            postal_code=shipping_data.postal_code,
            address=shipping_data.address,
            city=shipping_data.city,
            province=shipping_data.province
        )
        warehouse_shipping_info.save()

        return CreateWarehouseShippingInfo(warehouse_shipping_info=warehouse_shipping_info)
    
class UpdateWarehouseShippingInfo(Mutation):
    class Arguments:
        warehouse_id = graphene.ID(required=True)
        shipping_data = UpdateWarehouseShippingInfoInput(required=True)

    warehouse_shipping_info = graphene.Field(WarehouseShippingInfoType)

    def mutate(self, info, warehouse_id, shipping_data=None):
        warehouse_shipping_info = WarehouseShippingInfo.objects.get(warehouse__pk=warehouse_id)
        if shipping_data.postal_code is not None:
            warehouse_shipping_info.postal_code = shipping_data.postal_code
        if shipping_data.address is not None:
            warehouse_shipping_info.address = shipping_data.address
        if shipping_data.city is not None:
            warehouse_shipping_info.city = shipping_data.city
        if shipping_data.province is not None:
            warehouse_shipping_info.province = shipping_data.province
        warehouse_shipping_info.save()

class DeleteWarehouse(Mutation):
    class Arguments:
        warehouse_id = graphene.ID(required=True)

    delete_success = graphene.Boolean() # verify that the entity was deleted

    def mutate(self, info, warehouse_id):
        Warehouse.objects.filter(pk=warehouse_id).delete()
        return DeleteWarehouse(delete_success=True)

class Mutation(object):
    create_warehouse = CreateWarehouse.Field()
    create_warehouse_shippingInfo = CreateWarehouseShippingInfo.Field()
    update_warehouse_shipping_info = UpdateWarehouseShippingInfo.Field()
    delete_warehouse = DeleteWarehouse.Field()
