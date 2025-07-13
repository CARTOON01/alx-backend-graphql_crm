"""
This file is a reference to the actual settings file in alx_backend_graphql_crm.
The actual Django settings are located in alx_backend_graphql_crm/settings.py
"""

# Import from the main settings file
from alx_backend_graphql_crm.settings import *

# Verify that django_crontab is in INSTALLED_APPS
if 'django_crontab' not in INSTALLED_APPS:
    INSTALLED_APPS.append('django_crontab')

# Verify CRONJOBS configuration
if not hasattr(locals(), 'CRONJOBS') or not CRONJOBS:
    CRONJOBS = [
        ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ]
