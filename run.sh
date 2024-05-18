#!/bin/sh

# Start the Flask app in the background
python app.py &

# Start the Celery worker
celery -A models.call_model.celery worker -P gevent --loglevel=info