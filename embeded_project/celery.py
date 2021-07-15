from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'embeded_project.settings')
app = Celery('embeded_project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# add periodic task to send event health every day
app.conf.beat_schedule = {
    # Scheduler Name
    'feeding-order-ten-seconds': {
        'task': 'food_planner.periodic_tasks.food_order',
        # Schedule
        'schedule': 10.0,
        # 'args': (),
    },
    'reset-tanks-seconds': {
        'task': 'food_planner.periodic_tasks.reset_tanks',
        # Schedule
        'schedule': 180.0,
        # 'args': (),
    },

}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


