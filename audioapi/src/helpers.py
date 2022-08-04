import requests
import os
from urllib.parse import urlparse
from pathlib import PurePath
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

DEFAULT_CHUNK_SIZE = 65536


def is_url(path):
    if path:
        return urlparse(path).scheme != ""
    else:
        return False

def is_file(path):
    if not is_url(path):
        return PurePath(path).suffix != ""
    else:
        return False

def upload_file(src, dst):
    file_size = os.path.getsize(src)
    with open(src, "rb") as fd:
        with tqdm(desc=f"Uploading", total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
            reader_wrapper = CallbackIOWrapper(t.update, fd, "read")
            response = requests.put(dst, data=reader_wrapper)
            response.raise_for_status()

def download_file(src, dst, chunk_size=DEFAULT_CHUNK_SIZE):
    response = requests.get(src, stream=True)
    response.raise_for_status()

    file_size = None
    if 'Content-Length' in response.headers.keys() and \
        int(response.headers['Content-Length']) != 0:
        file_size = int(response.headers['Content-Length'])

    kwargs = dict(miniters=1, desc="Downloading", total=file_size)
    kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
    with tqdm.wrapattr(open(dst, "wb"), "write", **kwargsNotNone) as fd:
        for chunk in response.iter_content(chunk_size):
            fd.write(chunk)
