# serverless-challenge
Construir uma arquitetura serverless para análise de imagens.

![Screenshot](Architecture.png)

Esse projeto utiliza as seguintes tecnologias:

 - Python
 - Amazon S3
 - AWS Lambda
 - Amazon DynamoDB
 - Amazon API Gateway
 - Serverless Framework

## Funções

O projeto possui 4 funções.

### extractMetadata
Responsável por extrair o nome, tamanho e tipo da imagem carregada e registrar no banco de dados. Não é acessada por método GET.

Quando uma imagem (ou mais) no formato .jpg, .jpeg, .png ou .gif é carregada na pasta `uploads` do bucket na Amazon S3 o AWS Lambda dispara a função `extractMetadata`. Essa função  recebe no parâmetro `event` a chave do objeto e o seu tamanho. 

O formato do a imagem é extraída da chave do objeto, onde todas as letras são transformadas em minúsculas para evitar redundâncias como `.jpg` e `.JPG`.

A chave do objeto, seu tamanho e tipo são salvos na tabela `serverless-challenge-dev`.

> **Issue**
> Falta implementar a análise da largura e altura da imagem.

### getMetadata
Recebe como parâmetro o nome da imagem `{s3objectkey}` e retorna os metadados registrados no banco de dados.

    GET <url>/images/{s3objectkey}

No arquivo `serverless.yml` foi implementado um evento para cada formato de arquivo.

> **Issue**
> No banco de dados há o prefixo "uploads/" antes do nome da imagem. Porém ainda não consegui implementar uma chamada do tipo `uploads/arquivo.jpg`. No momento basta informar o nome do arquivo, sem o prefixo.

### infoImages
Retorna do banco de dados o arquivo de maior e menor tamanho, os formatos de imagens registradas e a quantidade de imagens em cada formato.

Não recebe nenhum parâmetro.

        GET <url>/infoimages

### getImage
Recebe como parâmetro o nome do arquivo e retorna um link temporário para download. Similar a `getMetadata`, aqui também deve-se informar apenas o nome do arquivo na url, sem o prefixo `uploads/`.

    GET <url>/get/{s3objectkey}

No arquivo `serverless.yml` foi acrescentado a função correspondente.

> **Issue**
> O link temporário para download está retornando acesso negado. Acredito que seja alguma permissão no meu usuário IAM para que possa dar acesso a essa função.