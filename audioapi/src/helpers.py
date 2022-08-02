import requests
import aiohttp
import aiofiles
import math
import os
from urllib.parse import urlparse
from pathlib import PurePath
from tqdm import tqdm


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

async def async_upload_from_file(src, dst):
    async with aiohttp.ClientSession() as session:
        await session.post(dst, data=file_sender(file_name=src))

def upload_from_file(src, dst):
    with open(src, 'rb') as src_fd:
        requests.put(dst, data=src_fd) 
        
async def url_sender(url=None, chunk_size=65536):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        print(resp)
        print(resp.headers)
        file_size = int(resp.headers['Content-Length'])
        progress = tqdm(desc=f"Uploading", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
        async for chunk in resp.content.iter_chunked(chunk_size):
            progress.update(len(chunk))
            yield chunk

async def upload_from_url(src, dst):
    async with aiohttp.ClientSession() as session:
        await session.post(dst, data=url_sender(src))

async def download_file(src_url, dest_file, chunk_size=65536):
    async with aiofiles.open(dest_file, 'wb') as fd:
        async with aiohttp.ClientSession() as session:
            async with session.get(src_url) as resp:
                print(resp)
                print(resp.headers)
                file_size = int(resp.headers['Content-Length'])
                progress = tqdm(desc=f"Downloading", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
                async for chunk in resp.content.iter_chunked(chunk_size):
                    await fd.write(chunk)
                    progress.update(len(chunk))

async def file_sender(file_name=None, chunk_size=65536):
    file_size = os.path.getsize(file_name)
    chunks = max(1, int(math.ceil(file_size / chunk_size)))
    progress = tqdm(desc=f"Uploading", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    async with aiofiles.open(file_name, 'rb') as f:
        for _ in range(chunks):
            chunk = await f.read(chunk_size)
            progress.update(len(chunk))
            yield chunk
