import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('studentData')

def lambda_handler(event, context):
    try:
        # Read studentid from query string parameters
        params     = event.get('queryStringParameters') or {}
        studentid  = params.get('studentid')

        if studentid:
            # Fetch a specific student
            result = table.get_item(Key={'studentid': studentid})
            item   = result.get('Item')
            if not item:
                return response(404, {'message': 'Student not found'})
            return response(200, item)
        else:
            # Fetch all students
            result = table.scan()
            return response(200, result.get('Items', []))

    except Exception as e:
        return response(500, {'message': str(e)})


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin':  '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(body)
    }
