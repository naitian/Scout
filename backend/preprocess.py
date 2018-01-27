import os

import youtube_dl
import scenedetect
import scenedetect.manager
import scenedetect.detectors
import cv2


def get_absolute_path(relative_path):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, relative_path)


def download_url(url, hook=None):
    if url is not list:
        url = [url]
    ydl_opts = {
        'format': 'bestvideo[height<=480]',
        'outtmpl': get_absolute_path('./videos/%(title)s.%(ext)s')
    }
    if hook:
        ydl_opts['progress_hooks'] = [hook]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def get_images(url):
    def finished(d):
        if d['status'] == 'finished':
            video_path = d['filename']
            print(video_path)
            os.makedirs(get_absolute_path('./frames/{}/'.format(video_path)), exist_ok=True)
            framerate, scene_list = get_frame_timestamps_stupid(video_path)
            write_frames_from_list(video_path, scene_list)

    download_url(url, hook=finished)


def get_frame_timestamps(filename):
    path = get_absolute_path('./videos/{}'.format(filename))
    content_detector = scenedetect.detectors.ContentDetector()
    smgr = scenedetect.manager.SceneManager(detector=content_detector)
    scenedetect.detect_scenes_file(path, smgr)
    video_framerate = 0
    return video_framerate, smgr.scene_list


def get_frame_timestamps_stupid(filename):
    path = get_absolute_path('./videos/{}'.format(filename))
    video = cv2.VideoCapture(path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.release()
    return fps, [x for x in range(0, length, fps * 3)]


def write_frames_from_list(filename, scene_list):
    print('Writing Images')
    path = get_absolute_path('./videos/{}'.format(filename))
    img_path_tpl = get_absolute_path('./frames/{}/'.format(filename))

    os.makedir(img_path_tpl, exist_ok=True)
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

# get_images_from_filename('It\'s Tentacle Time! -- Mind Blow #112.mp4')
# get_images('www.youtube.com/watch?v=PXd-sZb5oqA')
