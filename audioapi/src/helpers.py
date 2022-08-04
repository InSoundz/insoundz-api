import requests
import aiohttp
import aiofiles
import math
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

async def async_file_sender(file_name=None, chunk_size=DEFAULT_CHUNK_SIZE):
    file_size = os.path.getsize(file_name)
    chunks = max(1, int(math.ceil(file_size / chunk_size)))
    progress = tqdm(desc=f"Uploading", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    async with aiofiles.open(file_name, 'rb') as f:
        for _ in range(chunks):
            chunk = await f.read(chunk_size)
            progress.update(len(chunk))
            yield chunk
            
async def async_upload_from_file(src, dst):
    async with aiohttp.ClientSession() as session:
        await session.post(dst, data=async_file_sender(src))

def upload_from_file(src, dst):
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

async def async_download_file(src_url, dest_file, chunk_size=DEFAULT_CHUNK_SIZE):
    async with aiofiles.open(dest_file, 'wb') as fd:
        async with aiohttp.ClientSession() as session:
            async with session.get(src_url) as response:
                response.raise_for_status()

                file_size = None
                if 'Content-Length' in response.headers.keys() and \
                    int(response.headers['Content-Length']) != 0:
                    file_size = int(response.headers['Content-Length'])

                kwargs = dict(
                    desc="Downloading", total=file_size,
                    unit="B", unit_scale=True, unit_divisor=1024
                )
                kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}

                progress = tqdm(**kwargsNotNone)
                async for chunk in response.content.iter_chunked(chunk_size):
                    await fd.write(chunk)
                    progress.update(len(chunk))
