import graphene
from graphene_django import DjangoObjectType
import re
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Customer, Product, Order, OrderItem


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    products = graphene.List(ProductType)
    total_amount = graphene.Float()
    
    class Meta:
        model = Order
        fields = "__all__"
    
    def resolve_products(self, info):
        return [item.product for item in self.items.all()]
    
    def resolve_total_amount(self, info):
        return sum(item.product.price * item.quantity for item in self.items.all())


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = "__all__"


class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(required=False)


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime(required=False)


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)
    
    customer = graphene.Field(CustomerType)
    message = graphene.String()
    
    @staticmethod
    def validate_phone(phone):
        if phone:
            pattern = r'^\+?[0-9]{10,15}$|^[0-9]{3}-[0-9]{3}-[0-9]{4}$'
            if not re.match(pattern, phone):
                raise ValidationError("Invalid phone format. Use +1234567890 or 123-456-7890")
    
    def mutate(self, info, input):
        try:
            if Customer.objects.filter(email=input.email).exists():
                return CreateCustomer(customer=None, message="Email already exists")
            
            self.validate_phone(input.phone)
            
            customer = Customer(
                name=input.name,
                email=input.email,
                phone=input.phone
            )
            customer.save()
            
            return CreateCustomer(customer=customer, message="Customer created successfully")
        except ValidationError as e:
            return CreateCustomer(customer=None, message=str(e))
        except Exception as e:
            return CreateCustomer(customer=None, message=f"An error occurred: {str(e)}")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)
    
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, input):
        customers = []
        errors = []
        
        with transaction.atomic():
            for i, customer_data in enumerate(input):
                try:
                    if Customer.objects.filter(email=customer_data.email).exists():
                        errors.append(f"Customer {i+1}: Email {customer_data.email} already exists")
                        continue
                    
                    if customer_data.phone:
                        pattern = r'^\+?[0-9]{10,15}$|^[0-9]{3}-[0-9]{3}-[0-9]{4}$'
                        if not re.match(pattern, customer_data.phone):
                            errors.append(f"Customer {i+1}: Invalid phone format. Use +1234567890 or 123-456-7890")
                            continue
                    
                    customer = Customer(
                        name=customer_data.name,
                        email=customer_data.email,
                        phone=customer_data.phone
                    )
                    customer.save()
                    customers.append(customer)
                except Exception as e:
                    errors.append(f"Customer {i+1}: {str(e)}")
        
        return BulkCreateCustomers(customers=customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)
    
    product = graphene.Field(ProductType)
    
    def mutate(self, info, input):
        try:
            if input.price <= 0:
                raise ValidationError("Price must be positive")
            
            if input.stock is not None and input.stock < 0:
                raise ValidationError("Stock cannot be negative")
            
            product = Product(
                name=input.name,
                price=input.price,
                in_stock=(input.stock > 0 if input.stock is not None else True)
            )
            product.save()
            
            return CreateProduct(product=product)
        except Exception as e:
            raise Exception(f"Failed to create product: {str(e)}")


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)
    
    order = graphene.Field(OrderType)
    
    def mutate(self, info, input):
        try:
            try:
                customer = Customer.objects.get(pk=input.customer_id)
            except Customer.DoesNotExist:
                raise ValidationError(f"Customer with ID {input.customer_id} does not exist")
            
            if not input.product_ids or len(input.product_ids) == 0:
                raise ValidationError("At least one product must be selected")
            
            products = []
            for product_id in input.product_ids:
                try:
                    product = Product.objects.get(pk=product_id)
                    products.append(product)
                except Product.DoesNotExist:
                    raise ValidationError(f"Product with ID {product_id} does not exist")
            
            with transaction.atomic():
                order = Order(
                    customer=customer,
                )
                order.save()
                
                for product in products:
                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=1 
                    )
                    order_item.save()
            
            return CreateOrder(order=order)
        except ValidationError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Failed to create order: {str(e)}")


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    customer_by_id = graphene.Field(CustomerType, id=graphene.Int(required=True))
    
    all_products = graphene.List(ProductType)
    product_by_id = graphene.Field(ProductType, id=graphene.Int(required=True))
    
    all_orders = graphene.List(OrderType)
    order_by_id = graphene.Field(OrderType, id=graphene.Int(required=True))

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
