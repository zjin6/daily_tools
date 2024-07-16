import subprocess

def extract_video(video_with_audio_file, extracted_video_file):
    """
    Extracts the video track from a file containing both video and audio.

    Args:
        video_with_audio_file (str): Path to the input video file with audio.
        extracted_video_file (str): Path to the output video file without audio.
    """
    command = [
        'ffmpeg',
        '-i', video_with_audio_file,
        '-c', 'copy',
        '-an',  # Ignore the audio track
        extracted_video_file
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully extracted video from {video_with_audio_file} into {extracted_video_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting video: {e}")

def merge_video_audio(extracted_video_file, new_audio_file, output_file):
    """
    Merge an extracted video file and a new audio file into one output file using FFmpeg.

    Args:
        extracted_video_file (str): Path to the extracted video file without audio.
        new_audio_file (str): Path to the new audio file.
        output_file (str): Path to the output merged file.
    """
    command = [
        'ffmpeg',
        '-i', extracted_video_file,
        '-i', new_audio_file,
        '-c:v', 'copy',  # Copy the video codec
        '-c:a', 'aac',   # Encode audio to AAC
        '-strict', 'experimental',  # Allow experimental codecs
        output_file
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully merged {extracted_video_file} and {new_audio_file} into {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error merging files: {e}")

# Example usage
video_with_audio_file = 'input_with_audio.mp4'
new_audio_file = 'new_audio.mp3'
extracted_video_file = 'extracted_video.mp4'  # Intermediate file in .mp4 format
output_file = 'output_merged.mp4'  # Final output file in .mp4 format

# Step 1: Extract the video track
extract_video(video_with_audio_file, extracted_video_file)

# Step 2: Merge the extracted video track with the new audio file
merge_video_audio(extracted_video_file, new_audio_file, output_file)
