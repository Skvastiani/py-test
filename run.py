"""Entry point for running the crypto signals API."""

from crypto_signals import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
