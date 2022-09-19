from celery import Celery
import time
import os

celery_app = Celery("tasks", backend=os.getenv('BACKEND_URI'),
                    broker=os.getenv('BROKER_URI'))


@celery_app.task()
def generate_document():
    time.sleep(1)
