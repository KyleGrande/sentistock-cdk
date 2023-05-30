import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "BRK.B", "GOOG", "TSLA", "META", "XOM"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StockQuotes')
    
    results = []
    for ticker in tickers:
        response = table.get_item(Key={'ticker': ticker})
        if 'Item' in response:
            item = response['Item']
            results.append(item)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(results, default=str)
    }
