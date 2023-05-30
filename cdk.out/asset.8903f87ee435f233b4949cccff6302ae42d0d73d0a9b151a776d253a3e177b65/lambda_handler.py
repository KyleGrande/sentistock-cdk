import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserStocks')

def lambda_handler(event, context):
    # Extract the userId from the event
    userId = event['queryStringParameters']['userId']

    # Query the DynamoDB table using the userId
    response = table.get_item(
        Key={
            'user_cognito_id': userId,
        }
    )

    # Check if an item was found
    if 'Item' in response:
        # Return the user stocks as a JSON object
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'stocks': response['Item']['stocks'],
            })
        }
    else:
        # Return an error message
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'message': 'User not found'
            })
        }
