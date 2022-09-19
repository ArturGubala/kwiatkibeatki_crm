from flask import request
from flask.views import View

from .tasks import celery_app, generate_document


class GetStatusView(View):

    def dispatch_request(id: int):
        task_status = celery_app.AsyncResult(id)
        status = {"status": task_status}
        return status


class CreateDocumentView(View):

    '''
    Expected body format

    invoice_data = {
        'document': {
            'date': '01-01-2022',
            'number': '123456',
            'warehouse_from': 'glowny',
            'warehouse_to': 'stoisko',
            'created_by': 'Testowy Użytkownik'
        },
        'positions': [
            {
                'name': 'trapez 3',
                'qty': '10.0',
                'price': '2.50',
                'amout': '25.0'
            },
            {
                'name': 'trapez 3',
                'qty': '10.0',
                'price': '2.50',
                'amout': '25.0'
            },
            {
                'name': 'trapez 3'   task = func.delay()
                'amout': '25.0'
            },
            {
                'name': 'trapez 3',
                'qty': '10.0',
                'price': '2.50',
                'amout': '25.0'
            },
            {
                'name': 'trapez 3',
                'qty': '10.0',
                'price': '2.50',
                'amout': '25.0'
            },
            {
                'name': 'trapez 3',
                'qty': '10.0',
                'price': '2.50',
                'amout': '25.0'
            }
        ]
    }
    '''

    def dispatch_request():
        body = request.body

        task = generate_document.delay()

        return task.id
