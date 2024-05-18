# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /mls

ENV DATABASE_URI="postgresql://postgres:findmyself123@34.101.69.150:5432"
ENV SQLALCHEMY_DATABASE_URI=$DATABASE_URI
# ENV SOCKETIO_REDIS_URL = 
# ENV CELERY_BROKER_URL = 
# ENV RESULT_BACKEND = 
# ENV BROKER_CONNECTION_RETRY_ON_STARTUP =True

COPY requirements.txt requirements.txt
RUN pip install -U \
    pip
RUN pip install -r requirements.txt

COPY . .

# CMD ["python", "app.py"]
# ADD command to run celery 

# Make the run.sh script executable
RUN chmod +x run.sh

# Set the default command to run the run.sh script
CMD ["./run.sh"]

LABEL name="mls-lulus on time"
LABEL version="1.0.0"

EXPOSE 5000