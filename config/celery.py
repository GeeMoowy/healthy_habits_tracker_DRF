from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-habit-reminders-every-minute': {
        'task': 'habits.tasks.send_habit_reminder',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}

app.autodiscover_tasks()
