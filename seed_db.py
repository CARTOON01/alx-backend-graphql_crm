#!/usr/bin/env python
"""
This script populates the database with sample data for testing purposes.
"""

import os
import django
import random
from decimal import Decimal

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order, OrderItem

def create_customers():
    """Create sample customers"""
    customers_data = [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St, City, Country'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'phone': '+1987654321',
            'address': '456 Elm St, City, Country'
        },
        {
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'phone': '555-123-4567',
            'address': '789 Oak St, City, Country'
        }
    ]
    
    print("Creating customers...")
    created_customers = []
    for data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=data['email'],
            defaults=data
        )
        if created:
            print(f"Created customer: {customer.name}")
        else:
            print(f"Customer already exists: {customer.name}")
        created_customers.append(customer)
    
    return created_customers

def create_products():
    """Create sample products"""
    products_data = [
        {
            'name': 'Laptop',
            'description': 'High-performance laptop with 16GB RAM',
            'price': Decimal('999.99'),
            'stock': 10
        },
        {
            'name': 'Smartphone',
            'description': 'Latest smartphone with 128GB storage',
            'price': Decimal('699.99'),
            'stock': 15
        },
        {
            'name': 'Headphones',
            'description': 'Noise-canceling wireless headphones',
            'price': Decimal('149.99'),
            'stock': 20
        },
        {
            'name': 'Monitor',
            'description': '27-inch 4K monitor',
            'price': Decimal('349.99'),
            'stock': 8
        },
        {
            'name': 'Keyboard',
            'description': 'Mechanical gaming keyboard',
            'price': Decimal('89.99'),
            'stock': 12
        }
    ]
    
    print("Creating products...")
    created_products = []
    for data in products_data:
        product, created = Product.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"Created product: {product.name} (${product.price})")
        else:
            print(f"Product already exists: {product.name}")
        created_products.append(product)
    
    return created_products

def create_orders(customers, products):
    """Create sample orders"""
    if not customers or not products:
        print("Cannot create orders: No customers or products available")
        return []
    
    print("Creating orders...")
    created_orders = []
    
    # Create 1-2 orders for each customer
    for customer in customers:
        num_orders = random.randint(1, 2)
        for _ in range(num_orders):
            order = Order.objects.create(customer=customer)
            
            # Add 1-3 products to each order
            num_products = random.randint(1, 3)
            selected_products = random.sample(products, min(num_products, len(products)))
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )
            
            print(f"Created order {order.id} for {customer.name} with {len(selected_products)} products")
            created_orders.append(order)
    
    return created_orders

def seed_database():
    """Main function to seed the database"""
    print("Starting database seeding...")
    
    # Check if data already exists
    if Customer.objects.exists() and Product.objects.exists() and Order.objects.exists():
        print("Database already contains data. Skipping seeding.")
        return
    
    customers = create_customers()
    products = create_products()
    orders = create_orders(customers, products)
    
    print(f"\nDatabase seeding completed:")
    print(f"- {len(customers)} customers")
    print(f"- {len(products)} products")
    print(f"- {len(orders)} orders")

if __name__ == "__main__":
    seed_database()
