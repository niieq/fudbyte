from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery

# Setting the Default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fudbyte.settings')
app = Celery('fudbyte_celery')

# Using a String here means the worker will always find the configuration
# information
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

