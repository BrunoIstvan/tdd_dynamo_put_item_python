import json

from app.dynamo_service import DynamoService
from app.exceptions.custom_exceptions import BodyNotFoundException, PutItemException


class Process(object):

    def __init__(self):
        self.dynamo_service = DynamoService()

    def execute(self, event):

        try:
            body = self.validate_body(event)
            body = json.loads(body)
            result = self.dynamo_service.execute_put_item(body)
            return self.build_response(result)

        except PutItemException as e:
            pass

        except BodyNotFoundException as e:
            pass

    def validate_body(self, event):
        """
        Método que valida se o conteúdo da requisição foi enviado no parametro body
        Retorna o conteúdo em caso de sucesso
        :param event: Dicionário com os dados de entrada originados pelo chamador
        :return: Conteúdo da requisição
        :exception: BodyNotFoundException em caso de parâmetro não informado ou conteúdo vazio
        """
        if 'body' not in event or event['body'] is None:
            raise BodyNotFoundException('O conteúdo da requisição não foi encontrado')

        return event['body']

    def build_response(self, content):
        """
        Método que constrói a resposta da execução desse processo
        :param content: Conteúdo da resposta
        :return: Resposta no padrão do API Gateway
        """

        if content is not None and content == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({'Response': 'Success'})
            }

        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Erro ao realizar inclusão de registro na tabela'})
        }
