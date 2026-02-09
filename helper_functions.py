import httpx
import json
import os
from typing import Union

def check_or_make_dir(output_dir: str) -> None:
    """
    Checks if local folder exists and creates if it doesn't
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def download_as_json(
        json_object: Union[dict, list],
        output_dir: str,
        output_file_name: str) -> str:
    """
    Helper function to download dictionary or list as json
    """
    if not output_file_name.endswith(".json"):
        output_file_name += ".json"

    file_path = f"{output_dir}/{output_file_name}"

    with open(file_path, 'w', encoding='utf-8-sig') as f:
        json.dump(json_object, f, indent=2, ensure_ascii=False)

    return file_path

def patch_httpx():
    """
    Disable SSL verification for httpx.Client
    """

    def patched_init(self, *args, **kwargs):
        kwargs['verify'] = False
        return original_init(self, *args, **kwargs)

    original_init = httpx.Client.__init__
    httpx.Client.__init__ = patched_init

