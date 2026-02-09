from constants import (
    OtherFilter,
    VideoDurationFilter,
    VideoMediumUploadDateFilter,
    VideoShortUploadDateFilter,
    VideoSortOrder,
    VideoUploadDateFilter,
    VideoUploadDateSortedDurationFilter,
)
from typing import Union

from pytubefix import YouTube
from youtubesearchpython import CustomSearch


class YouTubeVideo():
    def __init__(self, url: str):
        self.url = url
        self.yt = YouTube(self.url)
        self.vid_length = self.yt.length
        self.vid_title = self.yt.title.replace(" ", "_")

    def download_youtube_video(
            self,
            output_dir: str = "output") -> str:
        """
        Download YouTube video to output folder

        Returns video file path 
        """

        print(f"Downloading video with URL: {self.url}")

        # Download video
        video_stream = self.yt.streams\
            .filter(progressive=True, file_extension='mp4')\
            .first()

        video_path = video_stream.download(
            output_path=output_dir,
            filename=f"{self.vid_title}.mp4")
        
        print(f"Video downloaded to: {video_path} is {self.vid_length}s long")
        
        return video_path

    def get_captions(self) -> dict:
        """
        Gets YouTube captions if available
        Returns Dictionary with caption and detected language
        """
        captions_obj = self.yt.captions
        if captions_obj:
            # Hard code caption language
            print(f"Retrieving caption with details {captions_obj}")
            captions_obj_s = str(captions_obj)
            lang = captions_obj_s.split(":")[0][2:-1]
            captions = captions_obj.get(lang, None)
        else:
            captions = None

        return {
            "captions_obj": captions_obj,
            "captions": captions
        }


def search_youtube(
        query: str,
        search_filters: Union[
            str,
            VideoSortOrder,
            VideoDurationFilter,
            VideoUploadDateFilter,
            VideoShortUploadDateFilter,
            VideoMediumUploadDateFilter,
            VideoUploadDateSortedDurationFilter,
            OtherFilter
        ],
        max_results: int = 10,
        max_pagination: int = 100) -> dict:
    """
    Search YouTube and return video information

    Args:
        query (str): Search keywords (can use Boolean NOT (-) and OR (|))
        search_filters: Based on Youtube URL Hashes found in Constants
        max_results (int): Maximum number of results to return
        max_pagination (int): Maximum number of pagination

    Returns:
        list: full List of dictionaries containing video info
    """
    # Perform search
    search = CustomSearch(
        query,
        searchPreferences=search_filters,
        language='en',
        region='SG',
        limit=max_results
    )

    # Extract relevant information
    videos_dict = []
    page_count, number_results = 0, 0

    while True:
        results = search.result()
        number_results += len(results['result'])
        page_count += 1

        for video in results['result']:
            videos_dict.append(video)

        # Move to next page
        has_next = search.next()

        if has_next is False:
            # Note that None may be returned despite existence of next page
            print("search.next() returned False. Exiting pagination.")
            break

        if number_results >= max_results:
            print(f"Number of results >= {max_results}. Exiting pagination.")
            break

        if page_count > max_pagination:
            print(f"Pagination reached {max_pagination}. Exiting")
            break

    return videos_dict
