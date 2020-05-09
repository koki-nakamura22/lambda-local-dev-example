# This function is the caller.
# 
# How to execute this file.
# Must upload this file and lambda_to_lambda_callee.py to AWS Lambda then executing them
# because it cannot execute another Lambda function locally.

import json
import boto3

def lambda_handler(event, context):
    response_body = {}
    execute_async_params = {
        'testKey': 'test parameter for executing async'
    }
    response_body['executeAsync'] = __executeAnotherLambdaAsync(execute_async_params)
    execute_sync_params = {
        'testKey': 'test parameter for executing sync'
    }
    response_body['executeSync'] = __executeAnotherLambdaSync(execute_sync_params)
    return {
        'statusCode': 200,
        'body': response_body
    }

# Executing another Lambda function async.
def __executeAnotherLambdaAsync(params):
    return __executeAnotherLambda(params, 'Event')

# Executing another Lambda function sync.
def __executeAnotherLambdaSync(params):
    return __executeAnotherLambda(params, 'RequestResponse')

# Executing another Lambda function.
def __executeAnotherLambda(params, invocation_type):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='lambda_to_lambda_callee',
        InvocationType=invocation_type,
        Payload=json.dumps(params)
    )
    pay_load = response['Payload'].read()
    pay_load_str = pay_load.decode('utf-8')
    if pay_load_str != '' and not pay_load_str is None:
        return json.loads(pay_load_str)
    else:
        return {}
