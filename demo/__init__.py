from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    from . import tasks

    @app.route('/')
    def index():
        return {'message': 'Demo app running'}

    @app.route('/users', methods=['POST'])
    def create_user():
        from flask import request
        data = request.get_json() or {}
        name = data.get('name')
        if not name:
            return {'error': 'Name required'}, 400
        user = models.User(name=name)
        db.session.add(user)
        db.session.commit()
        # enqueue background task
        tasks.send_welcome_email.delay(user.id)
        return {'id': user.id, 'name': user.name}, 201

    @app.route('/users')
    def list_users():
        users = models.User.query.all()
        return {'users': [{'id': u.id, 'name': u.name} for u in users]}

    return app
