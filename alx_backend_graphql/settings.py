"""
This file is a reference to the actual settings file in alx_backend_graphql_crm.
"""

# Import all settings from the actual settings file
from alx_backend_graphql_crm.settings import *

# Ensure graphene_django is in INSTALLED_APPS
if 'graphene_django' not in INSTALLED_APPS:
    INSTALLED_APPS.append('graphene_django')

# Ensure crm is in INSTALLED_APPS
if 'crm' not in INSTALLED_APPS:
    INSTALLED_APPS.append('crm')

# GraphQL Schema
GRAPHENE = {
    'SCHEMA': 'alx_backend_graphql.schema.schema'
}
