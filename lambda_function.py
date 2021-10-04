import json

from app.process import Process


def lambda_handler(event, context):
    return Process().execute(event)


if __name__ == '__main__':
    event = {
        'body': json.dumps({
            'cpf': '12345678900',
            'email': 'usuario1@gmail.com',
            'full_name': 'usuario 1 da silva',
            'state': 'SP',
            'city': 'São Paulo'
        })
    }

    lambda_handler(event, None)
