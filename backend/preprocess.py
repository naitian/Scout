import boto3
import cv2
from datetime import datetime
import os
import scenedetect
import scenedetect.manager
import scenedetect.detectors
import youtube_dl

def get_current_time_string():
    timestamp = datetime.now()
    return '%i_%i_%i' % (timestamp.hour, timestamp.minute, timestamp.second)

def get_absolute_path(relative_path):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, relative_path)


def download_url(url, hook=None):
    print('Start download video - %s' % get_current_time_string())
    if url is not list:
        url = [url]
    ydl_opts = {
        'format': 'bestvideo[height<=480]',
        'outtmpl': get_absolute_path(os.path.join('.', 'videos', '%(title)s.%(ext)s'))
    }
    if hook:
        ydl_opts['progress_hooks'] = [hook]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def update_video_index(url, title, framerate):
    dynamodb_client = boto3.client('dynamodb')
    tables_list = dynamodb_client.list_tables()
    if 'index' not in tables_list['TableNames']:
        dynamodb_client.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'url',
                    'AttributeType': 'S'
                }
            ],
            TableName='index',
            KeySchema=[
                {
                    'AttributeName': 'url',
                    'KeyType': 'HASH'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        dynamodb_client.get_waiter('table_exists').wait(TableName='index')
    response = dynamodb_client.put_item(
        TableName='index',
        Item={
            'url': {
                'S': url
            },
            'title': {
                'S': title
            },
            'framerate': {
                'N': str(int(framerate))
            }
        }
    )
    return response


def get_images(url):
    def finished(d):
        if d['status'] == 'finished':
            print('End download video - %s' % get_current_time_string())
            video_path = os.path.split(d['filename'])[-1]
            print(video_path)
            os.makedirs(get_absolute_path(os.path.join('.', 'frames', '{}').format(video_path)), exist_ok=True)
            framerate, scene_list = get_frame_timestamps_stupid(video_path)
            update_video_index(url, video_path, framerate)
            write_frames_from_list(video_path, scene_list)
    download_url(url, hook=finished)


def get_frame_timestamps(filename):
    path = get_absolute_path(os.path.join('.', 'videos', '{}').format(filename))
    content_detector = scenedetect.detectors.ContentDetector()
    smgr = scenedetect.manager.SceneManager(detector=content_detector)
    scenedetect.detect_scenes_file(path, smgr)
    video_framerate = 0
    return video_framerate, smgr.scene_list


def get_frame_timestamps_stupid(filename):
    path = get_absolute_path(os.path.join('.', 'videos', '{}').format(filename))
    video = cv2.VideoCapture(path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.release()
    return fps, [x for x in range(0, length, fps * 3)]


def write_frames_from_list(filename, scene_list):
    print('Writing Images')
    path = get_absolute_path(os.path.join('.', 'videos', '{}').format(filename))
    img_path_tpl = get_absolute_path(os.path.join('.', 'frames', '{}', '').format(filename))

    os.makedirs(img_path_tpl, exist_ok=True)
    cap = cv2.VideoCapture(path)
    ind = 0
    success = True
    while success:
        success, frame = cap.read()
        if ind in scene_list:
            image_path = img_path_tpl + 'frame{}.png'.format(ind)
            print('writing frame {} to {}'.format(ind, image_path))
            cv2.imwrite(image_path, frame)
        ind += 1
    cap.release()


def get_images_from_filename(filename):
    frame_rate, scene_list = get_frame_timestamps(filename)
    # frame_rate, scene_list = get_frame_timestamps_stupid(filename)
    write_frames_from_list(filename, scene_list)

if __name__ == '__main__':
    # get_images_from_filename('It\'s Tentacle Time! -- Mind Blow #112.mp4')
    get_images('www.youtube.com/watch?v=PXd-sZb5oqA')
