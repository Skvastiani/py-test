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

## Running locally on macOS

1. Install [Homebrew](https://brew.sh/) if it is not already available.
2. Install Python 3 and Redis:

```bash
brew install python redis
brew services start redis  # start Redis as a background service
```

3. (Optional) create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required Python packages:

```bash
pip install -r requirements.txt
```

5. Start the Flask application and the Celery worker in separate terminals:

```bash
python run.py
celery -A crypto_signals.tasks worker --loglevel=info
```

Once running, the API will be available at [http://localhost:5000](http://localhost:5000).
