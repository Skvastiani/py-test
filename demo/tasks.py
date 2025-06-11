"""Celery tasks for the demo application.

The Celery configuration is kept very small for the purposes of the tests in
this repository.  By default tasks are executed eagerly (synchronously) so that
running the test-suite does not require a running Redis broker.  In a real
deployment the broker URL can be overridden via the ``CELERY_BROKER_URL``
environment variable and ``CELERY_TASK_ALWAYS_EAGER`` set to ``False``.
"""

import os
from celery import Celery
from . import db
from .models import User

celery = Celery('demo')
celery.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', celery.conf.broker_url)
celery.conf.task_always_eager = os.getenv('CELERY_TASK_ALWAYS_EAGER', 'True') == 'True'

@celery.task
def send_welcome_email(user_id):
    user = User.query.get(user_id)
    if user:
        print(f"Sending welcome email to {user.name}")
        return True
    return False
