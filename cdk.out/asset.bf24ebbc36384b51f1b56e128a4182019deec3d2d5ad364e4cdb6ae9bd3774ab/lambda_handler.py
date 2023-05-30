import json
import boto3

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    # Extract the text from the event body
    body = json.loads(event['body'])
    text = body['text']

    # Call the detect_targeted_sentiment function
    sentiment_response = comprehend.detect_targeted_sentiment(
        Text=text,
        LanguageCode='en'
    )

    # Filter organizations and their sentiment
    organizations_sentiment = []
    for entity in sentiment_response['Entities']:
        for mention in entity['Mentions']:
            if mention['Type'] == 'ORGANIZATION':
                organization_sentiment = {
                    'Text': mention['Text'],
                    'Sentiment': mention['MentionSentiment']['Sentiment'],
                    'SentimentScore': mention['MentionSentiment']['SentimentScore']
                }
                organizations_sentiment.append(organization_sentiment)

    # Return the organizations and their sentiment
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(organizations_sentiment)
    }