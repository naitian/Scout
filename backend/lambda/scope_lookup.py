import boto3
import json

def lambda_handler(event: object, context: object) -> str:
    """Looks up url in DynamoDB index.

    Args:
        event: payload object containing url.
        context: context information.

    Returns:
        string: response payload that conforms to standards described here
            https://aws.amazon.com/premiumsupport/knowledge-center/malformed-502-api-gateway/.
    """
    response_payload = {
        'isBase64Encoded': 'false',
        'statusCode': 200,
        'headers': {},
        'body': ''
    }
    
    if 'queryStringParameters' not in event or 'url' not in event['queryStringParameters']:
        response_payload['body'] = 'Need to define "url" as a query parameter'
        return response_payload
    
    # Retrieve labels
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
    
    if 'Item' in response and 'labels' in response['Item']:
        # Format labels into objects with "keyword" and "timestamps"
        labels = json.loads(response['Item']['labels']['S'])
        label_objects = []
        for label in labels:
            label_objects.append({
                'keyword': label,
                'timestamps': labels[label]
            })
            
        response_payload['body'] = json.dumps(label_objects)
        return response_payload
    response_payload['body'] = 'Labels for this url are not available right now.'
    return response_payload