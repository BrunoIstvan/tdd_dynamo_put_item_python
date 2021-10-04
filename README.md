# tdd_dynamo_put_item_python

Criar virtualenv:

    pip install virtualenv
    virtualenv venv
    
Ativar virtualenv

    source venv/bin/activate

Instalar dependências:

    pip install -r requirements.txt

Rodar os testes unitários:

    pytest --cov=app tests/   

Criar arquivo zip para subir no lambda:

    zip -r dynamo_put_item_python.zip lambda_function.py app/* -x "*.pyc" -x ".pytest_cache"  

Desativar virtualenv

    deactivate

Atualizar código do lambda:

    aws lambda update-function-code --function-name tdd_dynamo_put_item --zip-file fileb://dynamo_put_item_python.zip

    