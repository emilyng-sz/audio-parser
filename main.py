from audioparser_module import (
    load_model,
    transcribe_with_fast_whisper
)
from filehandler_module import extract_audio
from helper_functions import (
    check_or_make_dir,
    download_as_json,
    patch_httpx
)

from youtube_module import YouTubeVideo

def transcribe_youtube_vid_pipeline(
        url: str,
        media_output_dir: str,
        json_output_dir: str,
        model) -> dict:
    """
    Download YouTube video to output folder
    """

    yt_module = YouTubeVideo(url)

    # Step 1: Download YouTube video
    video_path = yt_module.download_youtube_video(
        output_dir=media_output_dir
    )

    # (Optional) Get captions
    captions_dict = yt_module.get_captions()
    captions_obj = captions_dict.get("captions_obj")
    captions = captions_dict.get("captions")

    # (For logging)
    video_file_data_dict = {
        "url": url,
        "title": yt_module.vid_title,
        "length": yt_module.vid_length,
        "video_path": video_path,
        "caption_details": str(captions_obj),
        "caption_seg": captions.generate_srt_captions() if captions else None,
        "caption_txt": captions.generate_txt_captions() if captions else None
    }

    # (For logging) Download video file info as json
    download_as_json(
        json_object=video_file_data_dict,
        output_dir=json_output_dir,
        output_file_name=f"{yt_module.vid_title}_video_info.json"
    )

    # Step 2: Extract audio
    audio_file = extract_audio(video_file_data_dict, media_output_dir)

    # Step 3: Transcribe with Fast-Whisper (with language detection)
    whisper_result_dict = transcribe_with_fast_whisper(
        audio_path=audio_file,
        model=model
    )
    print(whisper_result_dict)

    # (For logging) Download transcription file info as json
    download_as_json(
        json_object=whisper_result_dict,
        output_dir=json_output_dir,
        output_file_name=f"{yt_module.vid_title}_transcription_info.json"
    )

    return 

if __name__ == '__main__':
    URL = "https://www.youtube.com/shorts/HzVnnNV2_Ck"
    # "https://www.youtube.com/shorts/l3FdOMS9PWE"
    # "https://www.youtube.com/watch?v=kTk__wy1xDc"
    # "https://www.youtube.com/watch?v=jbKaILNq9SI"
    MEDIA_OUTPUT_DIR = "media_files"
    JSON_OUTPUT_DIR = "json_output_files"
    MODEL_PATH = "../../faster-whisper-small"

    for output_dir in [MEDIA_OUTPUT_DIR, JSON_OUTPUT_DIR]:
        check_or_make_dir(output_dir=output_dir)

    patch_httpx()

    # Download load model from local folder
    model = load_model(model_name="faster-whisper-small")

    transcribe_youtube_vid_pipeline(
        url=URL,
        media_output_dir=MEDIA_OUTPUT_DIR,
        json_output_dir=JSON_OUTPUT_DIR,
        model=model
    )
    
