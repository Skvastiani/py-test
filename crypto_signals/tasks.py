import requests
from datetime import datetime
from . import celery, db, socketio
from .models import Signal
from .utils import moving_average, compute_rsi

BINANCE_API = 'https://api.binance.com/api/v3/klines'


def _fetch_closes(pair, limit=50, interval='1h'):
    params = {'symbol': pair.upper(), 'interval': interval, 'limit': limit}
    resp = requests.get(BINANCE_API, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [float(c[4]) for c in data]  # closing prices


@celery.task
def compute_signals(pair):
    closes = _fetch_closes(pair)
    ma_short = moving_average(closes, 7)
    ma_long = moving_average(closes, 25)
    rsi = compute_rsi(closes)
    signal = Signal(pair=pair.upper(), timestamp=datetime.utcnow(),
                    ma_short=ma_short, ma_long=ma_long, rsi=rsi)
    db.session.add(signal)
    db.session.commit()
    socketio.emit('signal', {
        'pair': pair.upper(),
        'ma_short': ma_short,
        'ma_long': ma_long,
        'rsi': rsi,
        'timestamp': signal.timestamp.isoformat()
    })
    return signal.id


@celery.task
def notify_users(signal_id):
    signal = Signal.query.get(signal_id)
    if not signal:
        return False
    # Placeholder for sending notifications
    print(f"Notify users about {signal.pair} signal at {signal.timestamp}")
    return True
