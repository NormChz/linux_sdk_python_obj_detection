import os
import argparse
from picamera2 import Picamera2, Preview

def run_parser():
    parser = argparse.ArgumentParser(
        prog='record.py',
        description='Record videos with RPI HQ cam and save to mp4 format at specified location',
        )
    parser.add_argument('file_name', help='Give a unique filename', type=str)
    parser.add_argument('duration', help='Give the duration in seconds', type=str)
    return parser.parse_args()

if __name__ == '__main__':

    args = run_parser()
    filename = args.file_name
    duration = int(args.duration)

    directory = os.path.dirname(__file__)
    video_folder = os.path.join(directory, f'videos_{filename}')
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)

    file_nrs = []
    for file in os.listdir(video_folder):
        file_nrs.append(int(file[(len(filename)+1):file.index('.')]))
    
    if (len(file_nrs) != 0):
        file_count = max(file_nrs) + 1
    else:
        file_count = 1

    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)

    new_file = os.path.join(video_folder, f'{filename}_{file_count}.mp4')
    if not os.path.exists(new_file):
        picam2.start_and_record_video(os.path.join(video_folder, f'{filename}_{file_count}.mp4'), duration=duration)
    else:
        raise Exception('A file with this name already exists')