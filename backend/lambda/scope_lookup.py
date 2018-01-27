import boto3

def lambda_handler(event: object, context: object) -> str:
    """Looks up url in DynamoDB index.

    Args:
        event: payload object containing url.
        context: context information.

    Returns:
        string: json string containing labels or empty if url not indexed.
    """
    dynamodb_client = boto3.client('dynamodb')
    
    response = dynamodb_client.get_item(
        TableName='index',
        Key={
            'url': {
                'S': event['url']
            }
        }
    )
    if 'Item' in response and 'labels' in response['Item']:
        return response['Item']['labels']['S']
    return "{}"