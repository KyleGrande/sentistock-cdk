import json
import boto3
# import requests

comprehend = boto3.client(service_name='comprehend')

def lambda_handler(event, context):
    # Extract the text from the event body
    body = json.loads(event['body'])
    text = body['text']

    # Analyze the text using Comprehend
    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')

    # Return the sentiment analysis result
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(sentiment_response, sort_keys=True, indent=4)
    }
