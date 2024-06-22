# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /mls

ENV DATABASE_URI="postgresql://postgres:findmyself123@34.101.69.150:5432"
ENV SQLALCHEMY_DATABASE_URI=$DATABASE_URI

COPY requirements.txt requirements.txt
RUN pip install -U \
    pip
RUN pip install -r requirements.txt

COPY . .

# # Make the run.sh script executable
# RUN chmod +x run.sh

# # Set the default command to run the run.sh script
# CMD ["./run.sh"]

CMD ["python", "app.py"]

LABEL name="mls-lulus on time"
LABEL version="1.0.0"

EXPOSE 5000