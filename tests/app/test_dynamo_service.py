from unittest import TestCase
from unittest.mock import MagicMock

from moto import mock_dynamodb2
from botocore.stub import Stubber

from app.dynamo_service import DynamoService
from app.exceptions.custom_exceptions import PutItemException

body = {
    'cpf': '233355522222',
    'email': 'usuario1@gmail.com',
    'full_name': 'usuario 1 da silva',
    'state': 'SP',
    'city': 'São Paulo',
    'active': False
}

item = {
    'cpf': {'S': body['cpf']},
    'email': {'S': body['email']},
    'full_name': {'S': body['full_name']},
    'state': {'S': body['state']},
    'city': {'S': body['city']},
    'actived': {'BOOL': body['active']}
}

item_resource = {
    'cpf': body['cpf'],
    'email': body['email'],
    'full_name': body['full_name'],
    'state': body['state'],
    'city': body['city'],
    'actived': body['active']
}


class TestDynamoService(TestCase):

    def setUp(self) -> None:
        self.service = DynamoService()

    def test_execute_put_item_success(self):
        client = self.service.get_client()
        assert client is not None

        # prepara um stubber
        with Stubber(client) as stubber:
            # recupera a resposta esperada da execucao do metodo put_item()
            response = {
                'ResponseMetadata': {
                    'HTTPStatusCode': 200
                }
            }

            # esses sao os parametros enviados ao metodo put_item()
            expected_params = {
                'TableName': 'User',
                'Item': item
            }

            stubber.add_response('put_item', response, expected_params)
            stubber.activate()
            # recebe a resposta do metodo contendo o status_code
            service_response = self.service.execute_put_item(body=body, client=client)
            assert service_response == response['ResponseMetadata']['HTTPStatusCode']

    def test_execute_put_item_exception(self):
        client = self.service.get_client()
        client.put_item = MagicMock(return_value=None)

        with self.assertRaises(PutItemException):
            # recebe a resposta do metodo contendo o conteudo e o tamanho do arquivo
            self.service.execute_put_item(client=client,
                                          body=body)

    @mock_dynamodb2
    def test_execute_put_item_table_success(self):
        resource = self.service.get_resource()
        assert resource is not None

        table_name = 'User'
        table = resource.create_table(TableName=table_name,
                                      KeySchema=[{'AttributeName': 'cpf', 'KeyType': 'HASH'}],
                                      AttributeDefinitions=[{'AttributeName': 'cpf', 'AttributeType': 'S'}])

        # recupera a resposta esperada da execucao do metodo put_item()
        response = {
            'ResponseMetadata': {
                'HTTPStatusCode': 200
            }
        }

        # recebe a resposta do metodo contendo o status_code
        service_response = self.service.execute_put_item_table(body=body, table=table)
        assert service_response == response['ResponseMetadata']['HTTPStatusCode']

    def test_execute_put_item_table_exception(self):
        resource = self.service.get_resource()
        table = resource.Table('User')
        table.put_item = MagicMock(return_value=None)

        with self.assertRaises(PutItemException):
            # recebe a resposta do metodo contendo o conteudo e o tamanho do arquivo
            self.service.execute_put_item_table(table=table, body=body)
