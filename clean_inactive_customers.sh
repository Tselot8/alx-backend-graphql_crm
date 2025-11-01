#!/bin/bash

PROJECT_DIR="/home/tselot88/projects"
LOG_FILE="/tmp/customer_cleanup_log.txt"

cd "$PROJECT_DIR" || exit

export DJANGO_SETTINGS_MODULE="alx_backend_graphql.settings"

DELETED_COUNT=$(python3 manage.py shell <<EOF
from crm.models import Customer
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta

cutoff_date = timezone.now() - timedelta(days=365)

# Annotate customers with last order date
inactive_customers = Customer.objects.annotate(
    last_order=Max('orders__order_date')
).filter(
    last_order__lt=cutoff_date
)

deleted_count = inactive_customers.count()
inactive_customers.delete()
print(deleted_count)
EOF
)

# Log the result to /customer_cleanup_log.txt
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"
