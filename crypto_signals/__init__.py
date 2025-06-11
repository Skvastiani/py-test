import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from celery import Celery


db = SQLAlchemy()
# SocketIO used for optional live updates via WebSocket
socketio = SocketIO(message_queue=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

celery = Celery(__name__)
celery.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', celery.conf.broker_url)
celery.conf.task_always_eager = os.getenv('CELERY_TASK_ALWAYS_EAGER', 'True') == 'True'


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crypto.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    from .api import bp
    app.register_blueprint(bp)

    return app
