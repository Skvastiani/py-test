# Crypto Trading Signals Platform

This project provides a small crypto trading signals API.  It exposes REST
endpoints for registering users and retrieving calculated signals for a trading
pair.  Price data is fetched from public APIs and indicators such as moving
averages and RSI are computed in background Celery tasks.  Signals can also be
pushed over WebSockets using **Flask-SocketIO**.

## Requirements

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

## Running the application

1. Ensure Redis is available (Docker Compose provides a ready to use setup).
2. Start the Flask application:

```bash
python run.py
```

3. In a separate terminal, run Celery:

```bash
celery -A crypto_signals.tasks worker --loglevel=info
```

You can then send `POST /register` requests with JSON `{"email": "user@example.com"}` to create users.  Signals for a pair can be retrieved from `/signals/<pair>`.
