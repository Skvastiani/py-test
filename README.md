# Demo Application

This repository contains a minimal demonstration app that uses **Flask**, **SQLAlchemy**, and **Celery**. It stores users in a SQLite database and processes a background task whenever a user is created.

## Requirements

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

## Running the application

1. Ensure Redis is running on `localhost:6379` for Celery.
2. Start the Flask application:

```bash
python run.py
```

3. In a separate terminal, run Celery:

```bash
celery -A demo.tasks worker --loglevel=info
```

You can then send `POST /users` requests with JSON `{"name": "Alice"}` to create users and trigger the background task.
