# How to execute this file.
# docker run --rm -v "$PWD":/var/task:ro,delegated lambci/lambda:python3.8 lambdas_with_docker.lambda_func_only.lambda_handler

import os
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
