# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /mls

ENV DATABASE_URI="postgresql://postgres:findmyself123@34.101.69.150:5432"
# ENV DATABASE_URI="postgresql://postgres:ta@host.docker.internal:5431"
ENV SQLALCHEMY_DATABASE_URI=$DATABASE_URI
ENV SOCKETIO_REDIS_URL="redis://34.128.94.15:6379/0"
ENV CELERY_BROKER_TRANSPORT_URL="redis://34.128.94.15:6379/0"
ENV RESULT_BACKEND="redis://34.128.94.15:6379/0"
ENV BROKER_CONNECTION_RETRY_ON_STARTUP=True

COPY requirements.txt requirements.txt
RUN pip install -U \
    pip
RUN pip install -r requirements.txt

COPY . .

# Make the run.sh script executable
RUN chmod +x run.sh

# Set the default command to run the run.sh script
CMD ["./run.sh"]

LABEL name="mls-lulus on time"
LABEL version="1.0.0"

EXPOSE 5000