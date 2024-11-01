import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'content_aggregator.settings')

import ssl
from django.conf import settings
from celery import Celery


app = Celery('content_aggregator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(f'django.conf:settings', namespace='CELERY')


# app.conf.broker_url = os.environ.get('REDIS_TLS_URL', 'redis://localhost:6379/0')
# app.conf.result_backend = os.environ.get('REDIS_TLS_URL', 'redis://localhost:6379/0')
app.conf.broker_url = 'rediss://:p98d90061dcbe89e6985697a5415dcf5d633e0ee0438679dc151aa464e3cab1b4@ec2-18-206-36-186.compute-1.amazonaws.com:20450'
app.conf.result_backend = 'rediss://:p98d90061dcbe89e6985697a5415dcf5d633e0ee0438679dc151aa464e3cab1b4@ec2-18-206-36-186.compute-1.amazonaws.com:20450'

app.conf.broker_transport_options = {
    'ssl_cert_reqs': 'CERT_NONE'  # or CERT_OPTIONAL, CERT_REQUIRED
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

