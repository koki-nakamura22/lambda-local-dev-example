# This function is the callee.
# 
# How to execute this file.
# Must upload this file and lambda_to_lambda_caller.py to AWS Lambda then executing them
# because it cannot execute another Lambda function locally.

import json

def lambda_handler(event, context):
    print(event['testKey'])
    return {
        'statusCode': 200,
        'body': json.dumps('Succeeded executing another Lambda function!')
    }
