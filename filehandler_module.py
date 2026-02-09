from moviepy import VideoFileClip
import os

def extract_audio(
        video_file_dct: dict,
        output_path: str = "output") -> str:
    """
    Extract audio from video file
    """

    file_name = video_file_dct["title"]
    video_path = video_file_dct["video_path"]

    print(f"Extracting audio from {video_path}")

    audio_file = os.path.join(output_path, f"{file_name}_audio.wav")

    # Load video and extract audio
    video = VideoFileClip(video_path)
    audio = video.audio

    # Export if needed
    audio.write_audiofile(audio_file)
    video.close()

    return audio_file

