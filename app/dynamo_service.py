import boto3

from app.exceptions.custom_exceptions import PutItemException


class DynamoService:

    def __init__(self):
        pass

    def get_client(self):
        """
        Método que retorna um client do Dynamo
        :return: Client do Dynamo
        """

        return boto3.client('dynamodb')

    def get_resource(self):
        """
        Método que retorna um resource do Dynamo
        :return: Resource do Dynamo
        """

        return boto3.resource('dynamodb', region_name='us-east-1')

    def execute_put_item(self, body, client=None):
        """
        Método que grava o conteúdo na tabela
        :param client:
        :param body: Conteúdo da tabela
        :return: Retorno da execução
        """

        if client is None:
            client = self.get_client()
        result = client.put_item(TableName='User',
                                 Item={
                                     'cpf': {'S': body['cpf']},
                                     'email': {'S': body['email']},
                                     'full_name': {'S': body['full_name']},
                                     'state': {'S': body['state']},
                                     'city': {'S': body['city']},
                                     'actived': {'BOOL': False}
                                 })

        if result is None:
            raise PutItemException('Inclusão de registro não executado com sucesso')

        status_code = result['ResponseMetadata']['HTTPStatusCode']

        # retorna o status code da execucao
        return status_code

    def execute_put_item_resource(self, body, resource=None):
        """
        Método que grava o conteúdo na tabela
        :param resource:
        :param body: Conteúdo da tabela
        :return: Retorno da execução
        """

        if resource is None:
            resource = self.get_resource()

        table = resource.Table('User')

        result = table.put_item(Item={
                                     'cpf': body['cpf'],
                                     'email': body['email'],
                                     'full_name': body['full_name'],
                                     'state': body['state'],
                                     'city': body['city'],
                                     'actived': False
                                 })

        if result is None:
            raise PutItemException('Inclusão de registro não executado com sucesso')

        status_code = result['ResponseMetadata']['HTTPStatusCode']

        # retorna o status code da execucao
        return status_code

    def execute_put_item_table(self, body, table):
        """
        Método que grava o conteúdo na tabela
        :param resource:
        :param body: Conteúdo da tabela
        :return: Retorno da execução
        """

        result = table.put_item(Item={
                                     'cpf': body['cpf'],
                                     'email': body['email'],
                                     'full_name': body['full_name'],
                                     'state': body['state'],
                                     'city': body['city'],
                                     'actived': False
                                 })

        if result is None:
            raise PutItemException('Inclusão de registro não executado com sucesso')

        status_code = result['ResponseMetadata']['HTTPStatusCode']

        # retorna o status code da execucao
        return status_code

