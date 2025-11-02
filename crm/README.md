# CRM Celery Report Setup

This guide explains how to configure Celery and Celery Beat to generate weekly CRM reports for your Django project.

## Setup Steps

1. **Install Redis and Python dependencies**
```bash
sudo apt install redis-server
pip install -r requirements.txt
```

2. **Run Django migrations**
```bash
python manage.py migrate
```

3. **Start Celery Worker**
```bash
celery -A crm worker -l info
```

4. **Start Celery Beat**
```bash
celery -A crm beat -l info
```

5. **Verify logs**
Check /tmp/crm_report_log.txt for weekly report entries. Each entry has the format:
```ruby
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
```

## Notes

- Ensure Redis is running before starting Celery worker and beat.

- Celery Beat is configured in crm/settings.py to run generatecrmreport every Monday at 06:00.

- The task fetches total customers, total orders, and total revenue via the GraphQL API and appends the report to the log file.