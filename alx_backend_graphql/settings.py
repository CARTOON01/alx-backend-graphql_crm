"""
This file is a reference to the actual settings file in alx_backend_graphql_crm.
"""

from alx_backend_graphql_crm.settings import *

if 'graphene_django' not in INSTALLED_APPS:
    INSTALLED_APPS.append('graphene_django')

if 'crm' not in INSTALLED_APPS:
    INSTALLED_APPS.append('crm')

GRAPHENE = {
    'SCHEMA': 'alx_backend_graphql.schema.schema'
}
