# coding=utf-8

import boto3
import botocore
from urllib.parse import unquote_plus
import decimalencoder
import json
from collections import Counter

dynamodb = boto3.resource("dynamodb")
s3 = boto3.resource('s3')

def extractMetadata(event, context):

    table = dynamodb.Table("serverless-challenge-dev")
    for record in event["Records"]:
        #bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        size = record['s3']['object']['size']      
        
        # gambiarra =(
        
        type_file = key.split('.')
        type_file = str(type_file[-1]).lower()
        
        # fim da gambiarra =)

        response = table.put_item(
            Item={
                's3objectkey': key,
                'size': size,
                "type": type_file
            }
        )
    
    return response


def getMetadata(event, context):
    
    s3objectkey = event["pathParameters"]["s3objectkey"]
    
    table = dynamodb.Table("serverless-challenge-dev")
    prefix = "uploads/"

    result = table.get_item(
        Key={
            "s3objectkey": prefix + s3objectkey
        }
    )
  
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                          cls=decimalencoder.DecimalEncoder)
    } 

    return response


def getImage(event, context):

    s3objectkey = event["pathParameters"]["s3objectkey"]
    prefix = "uploads/"
    bucket = "meusarquivosdodesafio"

    s3_client = boto3.client('s3')
    url = s3_client.generate_presigned_url('get_object', 
                Params = {"Bucket": bucket, "Key": prefix + s3objectkey}, ExpiresIn=100)

    response = {
        "statusCode": 200,
        "body": json.dumps({"URL": url})
    }
    
    return response


def infoImages(event, context):

    table = dynamodb.Table("serverless-challenge-dev")

    result = table.scan()
    result = result['Items']

    maior = max(result, key=lambda x:x['size'])
    menor = min(result, key=lambda x:x['size'])
    tipos_geral = list(d["type"] for d in result)
    tipos_numero = Counter(tipos_geral)

    resposta = {
        "maiorTamanho": maior,
        "menorTamanho": menor,
        "formatos": list(set(tipos_geral)),
        "quantidade": dict(tipos_numero)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(resposta,
                          cls=decimalencoder.DecimalEncoder)
        }

    return response