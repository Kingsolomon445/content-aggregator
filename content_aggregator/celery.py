import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'content_aggregator.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from django_celery_beat.models import PeriodicTask, IntervalSchedule

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

app.conf.update(BROKER_URL=os.environ.get('REDIS_URL'),
                CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL'))

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Interval schedule 
schedule, created = IntervalSchedule.objects.get_or_create(
    every=2,
    period=IntervalSchedule.MINUTES,
)

# Schedule tasks
PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch crypto content',
    task='blog.tasks.fetch_crypto_content',
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch tech jobs',
    task='blog.tasks.fetch_tech_jobs',
)
PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch cyber content',
    task='blog.tasks.fetch_cyber_content',
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch python jobs',
    task='blog.tasks.fetch_python_jobs',
)
PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch sd content',
    task='blog.tasks.fetch_sd_content',
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch ui_ux jobs',
    task='blog.tasks.fetch_ui_ux_jobs',
)
PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch mobile_pc content',
    task='blog.tasks.fetch_mobile_pc_content',
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Fetch general jobs',
    task='blog.tasks.fetch_general_jobs',
)

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
