import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retriever.settings')

app = Celery('retriever')    

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'task1-schedule': 
    # {
    #     'task': 'task1',
    #     'schedule': crontab(), # runs every minute
    #     'args': ([10])
    # },
    # 'task2-schedule':{
    #     'task': 'task2',
    #     'schedule': crontab(),
    #     'args': ([20])
    # },
}