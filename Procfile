web: gunicorn content_aggregator.wsgi

# Uncomment this `release` process if you are using a database, so that Django's model
# migrations are run as part of app deployment, using Heroku's Release Phase feature:
# https://docs.djangoproject.com/en/5.1/topics/migrations/
# https://devcenter.heroku.com/articles/release-phase
release: ./manage.py migrate --no-input

worker: celery -A content_aggregator worker --loglevel=info
beat: celery -A content_aggregator beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler