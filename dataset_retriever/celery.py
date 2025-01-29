import os
import logging
from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataset_retriever.settings')

app = Celery('dataset_retriever')    

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Ensure Celery uses Django's logging configuration
# @setup_logging.connect
# def config_loggers(*args, **kwags):
#     from logging.config import dictConfig
#     from django.conf import settings
#     dictConfig(settings.LOGGING)
#     logger = logging.getLogger('celery.task')
#     logger.info('Celery logging configured')

# @setup_logging.connect
# def configure_logging(loglevel, logfile, format, colorize, **kwargs):
#     handler = logging.StreamHandler()  # Logs to stdout
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logging.getLogger().addHandler(handler)
#     logging.getLogger().setLevel(loglevel)
#     logger = logging.getLogger('celery.task')
#     logger.setLevel(loglevel)
#     logger.addHandler(handler)
#     logger.propagate = True
#     logger.info('Celery logging configured')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'task1-schedule': 
    {
        'task': 'task1',
        # 'schedule': crontab(minute='*/5'), # runs every 5 minutes
        'schedule': crontab(), # runs every minute
        'args': ([10])
    },
    # 'task2-schedule':{
    #     'task': 'task2',
    #     'schedule': crontab(),
    #     'args': ([20])
    # },
}

