import boto3
import os

rekognition_client = boto3.client('rekognition')


def rekognize_objects_in_frame(video_title: str, frame_title: str) -> object:
    """Detect labels using AWS Rekognition.

    Args:
        video_title: name of video file.
        frame_title: name of frame png file.

    Returns:
        Rekognition detect labels response.
    """
    frame_png_filepath = os.path.join('frames', video_title, frame_title)

    frame_raw_bytes = open(frame_png_filepath, 'rb').read()
    response = rekognition_client.detect_labels(
        Image={
            'Bytes': frame_raw_bytes
        },
        MaxLabels=25,
        MinConfidence=50
    )
    return response


def list_pngs(video_title: str) -> list:
    """List png frame files for a video.

    Args:
        video_title: name of video file.

    Returns:
        List of png file names.

    """
    path_to_pngs = os.path.join('frames', video_title)
    files = os.listdir(path_to_pngs)
    png_files = [f for f in files if os.path.splitext(f)[1] == '.png']
    png_files = sorted(png_files, key=lambda s: int(s[5:-4]))
    return png_files


def get_labels_for_video(video_title: str, framerate: int) -> dict:
    """Label all provided frames for video.

    Args:
        video_title: name of video file
        framerate: framerate of video

    Returns:
        Map of label to list of times label appeared in video
    """
    frames = list_pngs(video_title)
    label_times = {}
    for f in frames:
        message = rekognize_objects_in_frame(video_title, f)
        seconds = int(f[5:-4]) / framerate
        minutes = seconds // 60
        display_seconds = seconds - minutes * 60
        labels = [label['Name'] for label in message['Labels']]
        for label in labels:
            if label not in label_times:
                label_times[label] = []
            label_times[label].append(seconds)
        print(minutes, ':', display_seconds, '|', ' '.join(labels))
    return label_times

if __name__ == '__main__':
    video_title = "It's Tentacle Time! -- Mind Blow #112.mp4"
    print(get_labels_for_video(video_title, 24))
