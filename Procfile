web: gunicorn --bind 127.0.0.1:8000 --workers=1 --threads=15 config.wsgi:application
websocket: daphne -b 127.0.0.1 -p 5000 config.asgi:application