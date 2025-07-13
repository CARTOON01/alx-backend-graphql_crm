#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

LOG_FILE="/tmp/customer_cleanup_log.txt"

if cd "$PROJECT_ROOT"; then
    echo "Successfully changed to project directory: $(pwd)"
else
    echo "Error: Failed to change to project directory: $PROJECT_ROOT"
    exit 1
fi

if [ -f "manage.py" ]; then
    echo "Found manage.py in current working directory (cwd): $(pwd)"
else
    echo "Error: manage.py not found in current working directory (cwd): $(pwd)"
    exit 1
fi

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
" 2>/dev/null)

if [ $? -eq 0 ]; then
    if [ -n "$DELETED_COUNT" ] && [ "$DELETED_COUNT" -ge 0 ]; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"
        echo "Customer cleanup completed. Deleted $DELETED_COUNT customers."
    else
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$TIMESTAMP] Warning: Unable to determine deletion count" >> "$LOG_FILE"
        echo "Customer cleanup executed but unable to determine deletion count."
    fi
else
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] Error: Failed to execute customer cleanup" >> "$LOG_FILE"
    echo "Error: Failed to execute customer cleanup script."
    exit 1
fi
