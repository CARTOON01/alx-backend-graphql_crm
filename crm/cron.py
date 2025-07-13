import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from django.conf import settings


def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm the CRM application's health.
    Also optionally queries the GraphQL hello field to verify the endpoint is responsive.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    heartbeat_message = f"{timestamp} CRM is alive\n"
    
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(heartbeat_message)
        
        try:
            query = {
                "query": "{ hello }"
            }
            
            data = json.dumps(query).encode('utf-8')
            
            req = urllib.request.Request(
                'http://localhost:8000/graphql/',
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if 'data' in result and 'hello' in result['data']:
                    graphql_status = f"{timestamp} GraphQL endpoint responsive: {result['data']['hello']}\n"
                    with open(log_file_path, "a") as log_file:
                        log_file.write(graphql_status)
                else:
                    error_message = f"{timestamp} GraphQL endpoint error: Invalid response format\n"
                    with open(log_file_path, "a") as log_file:
                        log_file.write(error_message)
                        
        except Exception as graphql_error:
            error_message = f"{timestamp} GraphQL endpoint error: {str(graphql_error)}\n"
            with open(log_file_path, "a") as log_file:
                log_file.write(error_message)
                
    except Exception as e:
        print(f"Failed to write heartbeat log: {str(e)}")
