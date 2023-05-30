import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserStocks')

def lambda_handler(event, context):
    # Extract the ticker and userId from the event body
    body = json.loads(event['body'])
    ticker = body['ticker']
    userId = body['userId']

    # Check if the user exists and has the stock
    response = table.get_item(
        Key={
            'user_cognito_id': userId,
        }
    )

    if 'Item' in response:
        # User exists, check if the stock exists in the user's portfolio
        if ticker in response['Item']['stocks']:
            # Stock exists for the user, remove the stock from the user's portfolio
            updated_stocks = [stock for stock in response['Item']['stocks'] if stock != ticker]

            table.update_item(
                Key={
                    'user_cognito_id': userId,
                },
                UpdateExpression='SET stocks = :updated_stocks',
                ExpressionAttributeValues={
                    ':updated_stocks': updated_stocks
                }
            )

            # Return a success response
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({
                    'message': 'Stock removed successfully',
                    'ticker': ticker
                })
            }
        else:
            # Stock does not exist for the user, return an error response
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Stock not found for the user'
                })
            }
    else:
        # User does not exist, return an error response
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'User not found'
            })
        }
