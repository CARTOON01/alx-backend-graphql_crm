"""
This file is a reference to the actual schema file in alx_backend_graphql_crm.
"""

import graphene
from graphene_django import DjangoObjectType
from crm.models import Customer, Product, Order, OrderItem
from alx_backend_graphql_crm.schema import Query as CRMQuery


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = '__all__'


class Query(CRMQuery, graphene.ObjectType):
    # Additional fields can be added here
    pass


schema = graphene.Schema(query=Query)
