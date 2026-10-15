import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('studentData')

def lambda_handler(event, context):
    try:
        # Read body from proxy integration
        body = json.loads(event['body'])

        studentid = body.get('studentid')
        name      = body.get('name')
        course    = body.get('course')
        email     = body.get('email')

        if not studentid:
            return response(400, {'message': 'studentid is required'})

        table.put_item(Item={
            'studentid': studentid,
            'name':      name,
            'course':    course,
            'email':     email
        })

        return response(200, {'message': 'Student data inserted successfully'})

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
