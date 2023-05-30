import boto3
import json
import decimal
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError
    
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StockQuotes')

    response = table.scan()
    items = response['Items']

    # Sort items by avg_sentiment in descending order
    sorted_items = sorted(items, key=lambda x: float(x['avg_sentiment']), reverse=True)

    # Get the top 10 items
    top_10_items = sorted_items[:10]

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(top_10_items, default=decimal_default)
    }
