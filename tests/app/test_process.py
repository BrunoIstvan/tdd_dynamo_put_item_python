import json
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from app.exceptions.custom_exceptions import BodyNotFoundException
from app.process import Process

content_file = {'cpf': '12345678900',
                'email': 'usuario1@gmail.com',
                'full_name': 'usuario 1 da silva',
                'state': 'SP',
                'city': 'São Paulo'}

event = {
    'body': json.dumps(content_file)
}

resp = {
    'ResponseMetadata': {
        'HTTPStatusCode': 200
    }
}


class TestProcess(TestCase):

    def setUp(self):
        self.process = Process()

    def test_execute_success(self):
        expected_response = self.process.build_response(content=resp['ResponseMetadata']['HTTPStatusCode'])
        self.process.validate_body = Mock(return_value=json.dumps(content_file))
        self.process.dynamo_service = MagicMock()
        self.process.dynamo_service.boto3.client = MagicMock()
        self.process.dynamo_service.execute_put_item = \
            MagicMock(return_value=resp['ResponseMetadata']['HTTPStatusCode'])

        response = self.process.execute(event)

        assert response == expected_response

        self.process.validate_body.assert_called_with(event)
        self.process.dynamo_service.execute_put_item.assert_called_with(content_file)

    def test_validate_body_success(self):
        response = self.process.validate_body(event)
        expected_response = json.dumps(content_file)

        assert response == expected_response, 'O retorno do método validate_body não condiz com o esperado'

    def test_validate_body_fail(self):
        with self.assertRaises(BodyNotFoundException):
            self.process.validate_body({})

    def test_build_response_success(self):

        expected_response = {
                'statusCode': 200,
                'body': json.dumps({'Response': 'Success'})
            }
        response = self.process.build_response(200)
        assert response == expected_response

    def test_build_response_internal_server_error(self):

        expected_response = {
            'statusCode': 500,
            'body': json.dumps({'message': 'Erro ao realizar inclusão de registro na tabela'})
        }
        response = self.process.build_response(None)
        assert response == expected_response

        response = self.process.build_response('anything different of 200')
        assert response == expected_response

