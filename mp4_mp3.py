import os
import glob
from moviepy.editor import AudioFileClip, VideoFileClip



def get_filepaths(folder, suffix='.mp4'):
    filepaths = glob.glob(os.path.join(folder, '*' + suffix))
    print(f'found {len(filepaths)} {suffix} files.')
    return filepaths


def trans_suffix(filepath, suffix='.mp3'):
    base_name, extension = os.path.splitext(filepath)
    trans_filepath = f'{base_name}{suffix}'
    # print(trans_filepath)
    return trans_filepath


def mp4_mp3(mp4_filepath):
    video = VideoFileClip(mp4_filepath)
    audio = video.audio
    audio = audio.set_fps(22050)
    trans_filepath = trans_suffix(mp4_filepath)
    audio.write_audiofile(trans_filepath)
    video.close()
    audio.close()
    return None


