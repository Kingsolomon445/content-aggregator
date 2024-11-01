import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'content_aggregator.settings')

from django.conf import settings
from celery import Celery


app = Celery('content_aggregator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(f'django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

