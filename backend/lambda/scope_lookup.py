import boto3
import json

def lambda_handler(event: object, context: object) -> str:
    """Looks up url in DynamoDB index.

    Args:
        event: payload object containing url.
        context: context information.

    Returns:
        string: json string containing labels or empty if url not indexed.
    """
    print(event)
    url = event['queryStringParameters']['url']
    dynamodb_client = boto3.client('dynamodb')
    
    response = dynamodb_client.get_item(
        TableName='index',
        Key={
            'url': {
                'S': url
            }
        }
    )
    response_payload = {
        'isBase64Encoded': 'false',
        'statusCode': 200,
        'headers': {},
        'body': ''
    }
    if 'Item' in response and 'labels' in response['Item']:
        labels = json.loads(response['Item']['labels']['S'])
        label_objects = []
        for label in labels:
            label_objects.append({
                'keyword': label,
                'timestamps': labels[label]
            })
            
        response_payload['body'] = json.dumps(label_objects)
        return response_payload
    response_payload['statusCode'] = 404
    return response_payload