import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('service')

app.config_from_object('django.conf.settings')

app.conf.broker_url = settings.CELERY_BROCKER_URL

app.autodiscover_tasks()
