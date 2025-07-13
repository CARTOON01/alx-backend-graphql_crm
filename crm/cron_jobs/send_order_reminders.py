#!/usr/bin/env python3

import os
import sys
import django
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup Django environment
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

def send_order_reminders():
    """
    Query GraphQL endpoint for pending orders within the last 7 days
    and log reminders to /tmp/order_reminders_log.txt
    """
    log_file = "/tmp/order_reminders_log.txt"
    graphql_endpoint = "http://localhost:8000/graphql"
    
    try:
        # Create GraphQL client
        transport = RequestsHTTPTransport(url=graphql_endpoint)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Define GraphQL query
        query = gql("""
            query {
                pendingOrdersLastWeek {
                    id
                    dateOrdered
                    status
                    customer {
                        id
                        name
                        email
                    }
                }
            }
        """)
        
        # Execute query
        result = client.execute(query)
        
        # Process results and log reminders
        orders = result.get('pendingOrdersLastWeek', [])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(log_file, 'a') as f:
            if orders:
                for order in orders:
                    customer = order.get('customer', {})
                    order_id = order.get('id')
                    customer_email = customer.get('email', 'N/A')
                    customer_name = customer.get('name', 'N/A')
                    date_ordered = order.get('dateOrdered', 'N/A')
                    
                    log_message = f"[{timestamp}] REMINDER: Order ID {order_id} - Customer: {customer_name} ({customer_email}) - Ordered: {date_ordered}\n"
                    f.write(log_message)
            else:
                log_message = f"[{timestamp}] No pending orders found in the last 7 days\n"
                f.write(log_message)
        
        print("Order reminders processed!")
        
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_message = f"[{timestamp}] ERROR: Failed to process order reminders - {str(e)}\n"
        
        with open(log_file, 'a') as f:
            f.write(error_message)
        
        print(f"Error processing order reminders: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    send_order_reminders()
