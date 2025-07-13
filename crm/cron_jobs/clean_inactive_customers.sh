#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

LOG_FILE="/tmp/customer_cleanup_log.txt"

cd "$PROJECT_ROOT"

DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders in the last year
customers_to_delete = Customer.objects.filter(
    orders__isnull=True
).union(
    Customer.objects.exclude(
        orders__date_ordered__gte=one_year_ago
    ).filter(
        orders__date_ordered__lt=one_year_ago
    )
).distinct()

# Count and delete
count = customers_to_delete.count()
customers_to_delete.delete()

print(count)
")

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"

echo "Customer cleanup completed. Deleted $DELETED_COUNT customers."
