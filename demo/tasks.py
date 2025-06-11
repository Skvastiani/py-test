from celery import Celery
from . import db
from .models import User

celery = Celery('demo', broker='redis://localhost:6379/0')

@celery.task
def send_welcome_email(user_id):
    user = User.query.get(user_id)
    if user:
        print(f"Sending welcome email to {user.name}")
        return True
    return False
