import json
import urllib.request
from decimal import Decimal
import boto3
from datetime import datetime

def lambda_handler(event, context):
    api_key = "JE4GXUURLWA6DGLJ"
    ticker = event['queryStringParameters']['ticker']

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    quote = data.get('Global Quote', {}).get('05. price')

    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())

    sum_scores = 0
    count_ticker = 0
    for feed in data['feed']:
        for ticker_sentiment in feed['ticker_sentiment']:
            if ticker_sentiment['ticker'] == ticker:
                ticker_sentiment_score = ticker_sentiment['ticker_sentiment_score']
                sum_scores += Decimal(ticker_sentiment_score)
                count_ticker += 1

    avg_score = sum_scores / count_ticker
    sentiment = ''
    if (avg_score <= -.35):
        sentiment = 'Bearish'
    elif (avg_score <= -.15):
        sentiment = 'Somewhat Bearish'
    elif (avg_score >= .35):
        sentiment = 'Bullish'
    elif (avg_score >= .15):
        sentiment = 'Somewhat Bullish'
    else:
        sentiment = 'Neutral'

    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StockQuotes')
    table.put_item(Item={
        'ticker': ticker,
        'quote': quote,
        'sentiment': sentiment,
        'avg_sentiment': str(avg_score),
        'timestamp': timestamp
    })

    response_data = {
        'ticker': ticker,
        'quote': quote,
        'sentiment': sentiment,
        'avg_sentiment': str(avg_score),
        'timestamp': timestamp
    }

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(response_data)
    }
