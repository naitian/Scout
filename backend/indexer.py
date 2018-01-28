import boto3
import frame_rekognition
import json
import preprocess
from shutil import rmtree
import sys

def extract_frames_from_video(video_url: str) -> None:
    """Extract frames from video using preprocessor.

    Args:
        video_url: url of Youtube video.
    """
    preprocess.get_images(video_url)

def get_metadata_of_video(video_url: str) -> tuple:
    """Retrieves metadata from DynamoDB about video.    

    Args:
        video_url: url of Youtube video.

    Returns:
        video_url: url of Youtube video.
        video_title: title of folder where video stored.
        video_framerate: frames per second of video.
    """
    dynamodb_client = boto3.client('dynamodb')
    get_item_response = dynamodb_client.get_item(
        TableName='index',
        Key={
            'url': {
                'S': video_url
            }
        }
    )
    video_title = get_item_response['Item']['title']['S']
    video_framerate = int(get_item_response['Item']['framerate']['N'])
    return video_url, video_title, video_framerate

def save_labels(video_url: str, video_title: str, video_framerate: int) -> None:
    """Detects and saves labels in DynamoDB for video.

    Args:
        video_url: url of Youtube video.
        video_title: title of folder where video stored.
        video_framerate: frames per second of video. 
    """
    labels = frame_rekognition.get_labels_for_video(video_title, video_framerate)
    labels_json = json.dumps(labels)

    dynamodb_client = boto3.client('dynamodb')
    update_item_response = dynamodb_client.update_item(
        TableName='index',
        Key={
            'url': {
                'S': video_url
            }
        },
        ExpressionAttributeNames={
            '#L': 'labels'
        },
        ExpressionAttributeValues={
            ':l': {
                'S': labels_json
            }
        },
        ReturnValues='ALL_NEW',
        UpdateExpression='SET #L = :l'
    )

def delete_media():
    """Delete frames and videos stored locally.
    """
    rmtree('frames/')
    rmtree('videos/')

def index_video(video_url):
    """Index labels of Youtube video into DynamoDB.

    Args:
        video_url: url of Youtube video.
    """
    extract_frames_from_video(video_url)
    url, title, framerate = get_metadata_of_video(video_url)
    save_labels(url, title, framerate)
    delete_media()

if __name__ == '__main__':
    assert len(sys.argv) == 2
    index_video(sys.argv[1])
