from flask import Blueprint, request
from .models import User, Signal
from . import db

bp = Blueprint('api', __name__)


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return {'error': 'email required'}, 400
    user = User(email=email, telegram_id=data.get('telegram_id'))
    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'email': user.email}, 201


@bp.route('/signals/<pair>')
def get_signals(pair):
    signals = (Signal.query.filter_by(pair=pair)
               .order_by(Signal.timestamp.desc())
               .limit(10)
               .all())
    return {
        'pair': pair,
        'signals': [
            {
                'timestamp': s.timestamp.isoformat(),
                'ma_short': s.ma_short,
                'ma_long': s.ma_long,
                'rsi': s.rsi,
            }
            for s in signals
        ]
    }
