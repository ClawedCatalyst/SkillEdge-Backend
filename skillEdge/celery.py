from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillEdge.settings')

app = Celery('skillEdge')
app.conf.enable_utc = False

app.conf.update(timezone = 'UTC')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
   'delete-every-10-minute': {
        'task': 'base.tasks.delete_unwanted_email',
        'schedule': crontab(minute='*/10'),
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')