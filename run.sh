#!/bin/sh

# Ensure environment variables are set correctly
export DATABASE_URI="postgresql://postgres:findmyself123@34.101.69.150:5432"
# export DATABASE_URI="postgresql://postgres:ta@host.docker.internal:5431"
export SQLALCHEMY_DATABASE_URI=$DATABASE_URI
export SOCKETIO_REDIS_URL="redis://34.101.77.142:6379/0"
export CELERY_BROKER_URL="redis://34.101.77.142:6379/0"
export RESULT_BACKEND="redis://34.101.77.142:6379/0"
export BROKER_CONNECTION_RETRY_ON_STARTUP=True

# Start the Celery worker
celery -A models.call_model.celery worker -P gevent --loglevel=info &

# Start the Flask app in the background
python app.py