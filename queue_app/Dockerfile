FROM python:3.9.13-alpine3.16
WORKDIR /queue_app
COPY .requirements/queue-requirements.txt .
RUN pip install -r queue-requirements.txt
COPY . .
ENV FLASK_APP=.
ENV FLASK_ENV=development