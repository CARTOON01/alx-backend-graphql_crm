"""
This file is a reference to the actual schema file in alx_backend_graphql_crm.
"""

import graphene
from graphene_django import DjangoObjectType
from crm.models import Customer, Product, Order, OrderItem


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


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")
    
    all_customers = graphene.List(CustomerType)
    customer_by_id = graphene.Field(CustomerType, id=graphene.Int(required=True))
    
    all_products = graphene.List(ProductType)
    product_by_id = graphene.Field(ProductType, id=graphene.Int(required=True))
    
    all_orders = graphene.List(OrderType)
    order_by_id = graphene.Field(OrderType, id=graphene.Int(required=True))

    def resolve_hello(self, info):
        return "Hello, GraphQL!"
        
    def resolve_all_customers(self, info):
        return Customer.objects.all()
        
    def resolve_customer_by_id(self, info, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return None
            
    def resolve_all_products(self, info):
        return Product.objects.all()
        
    def resolve_product_by_id(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
            
    def resolve_all_orders(self, info):
        return Order.objects.all()
        
    def resolve_order_by_id(self, info, id):
        try:
            return Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
