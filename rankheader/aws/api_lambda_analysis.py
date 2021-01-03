"""Lambda function handler for API."""
import os
import logging
import json
import boto3
import uuid

#from aws_xray_sdk.core import patch_all

#patch_all()

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
LOGGER.info('region: %s', REGION)

SQS_NAME = os.environ.get('SQS_NAME', 'rankheader_queue')
LOGGER.info('SQS name: %s', SQS_NAME)

DB_TABLE = os.environ.get('DB_TABLE', 'rankheader_state')
LOGGER.info('DB table: %s', DB_TABLE)

try:
    LOGGER.info('initializing boto3 SQS client')
    SQS = boto3.resource(service_name='sqs', region_name=REGION)
    QUEUE = SQS.get_queue_by_name(QueueName=SQS_NAME)
    LOGGER.info('boto3 SQS client initialized')
except BaseException as error:
    LOGGER.info('error initializing boto3 SQS client: %s', error)
    raise

try:
    LOGGER.info('initializing boto3 DYNAMODB client')
    DYNAMODB = boto3.resource(service_name='dynamodb', region_name=REGION)
    TABLE = DYNAMODB.Table(DB_TABLE)
    LOGGER.info('boto3 DYNAMODB client initialized')
except BaseException as error:
    LOGGER.error('error initializing boto3 DYNAMODB client: %s', error)
    raise

def __create_result(status_code, response_body):
    return {
        'isBase64Encoded': False,
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response_body)
    }

def __get(event, context):
    try:
        operation_id = event['queryStringParameters']['id']
        LOGGER.info('getting operation: %s', operation_id)
        response = TABLE.get_item(Key={'id': operation_id})
        LOGGER.info('get response: %s', response)
        response_body = response['Item']
        status_code = 200
    except BaseException as error:
        status_code = 500
        response_body = { 'error': 'An internal server error occurred.'}
        LOGGER.error('error getting state: %s', error)

    return __create_result(status_code, response_body)

def __post(event, context):
    try:
        num_sites = int(event['queryStringParameters']['num_sites'])
        num_headers = int(event['queryStringParameters']['num_headers'])

        operation_id = str(uuid.uuid4())
        operation = {
            'id' : operation_id,
            'num_sites' : num_sites,
            'num_headers' : num_headers,
        }
        
        LOGGER.info('enqueueing operation: %s', operation_id)
        response = QUEUE.send_message(MessageBody=json.dumps(operation))
        LOGGER.info('enqueue response: %s', response)
        
        LOGGER.info('persisting operation: %s', operation_id)
        operation['status'] = 'received'
        response = TABLE.put_item(Item=operation)
        LOGGER.info('persist response: %s', response)

        status_code = 200
        response_body = { 'id' : operation_id }
    except BaseException as error:
        status_code = 500
        response_body = { 'error': 'An internal server error occurred.'}
        LOGGER.error('error enqueueing operation: %s', error)

    return __create_result(status_code, response_body)

def lambda_handler(event, context):
    """Lambda function handler for API."""
    LOGGER.info('processing event %s', event)

    method = event['httpMethod']
    if method == 'GET':
        return __get(event, context)
    elif method == 'POST':
        return __post(event, context)
    else:
        return __create_result(500, 'Unsupported method')