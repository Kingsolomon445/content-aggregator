import os
import ssl
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'content_aggregator.settings')


from django.conf import settings
from celery import Celery
# from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'content_aggregator.settings')
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

app = Celery('content_aggregator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(f'django.conf:settings', namespace='CELERY')


app.conf.broker_url = os.environ.get('REDIS_TLS_URL', 'redis://localhost:6379/0')
app.conf.result_backend = os.environ.get('REDIS_TLS_URL', 'redis://localhost:6379/0')

app.conf.broker_transport_options = {
    'ssl_cert_reqs': 'CERT_NONE'  # or CERT_OPTIONAL, CERT_REQUIRED
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

