import json
import boto3
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserStocks')

def lambda_handler(event, context):
    # Extract the ticker and userId from the event body
    body = json.loads(event['body'])
    ticker = body['ticker']
    userId = body['userId']

    # Check if the user already has the stock
    response = table.get_item(
        Key={
            'user_cognito_id': userId,
        }
    )

    if 'Item' in response:
        # User exists, check if the stock already exists in the user's portfolio
        if ticker in response['Item']['stocks']:
            # Stock already exists for the user, return an error response
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Stock already exists for the user'
                })
            }
        else:
            # Add the new stock to the user's portfolio
            table.update_item(
                Key={
                    'user_cognito_id': userId,
                },
                UpdateExpression='SET stocks = list_append(stocks, :new_stock)',
                ExpressionAttributeValues={
                    ':new_stock': [ticker]
                }
            )
    else:
        # User does not exist, create a new item with the stock
        timestamp = datetime.utcnow().isoformat()
        item = {
            'user_cognito_id': userId,
            'stocks': [ticker],
        }

        table.put_item(Item=item)

    # Return the newly added stock data
        # Return the newly added stock data
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },  # Add comma here
        'body': json.dumps({
            'ticker': ticker,
        })
    }
