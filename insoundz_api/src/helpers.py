import requests
import os
import sys
import logging
import validators
import shutil
from pathlib import PurePath
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

DEFAULT_CHUNK_SIZE = 65536
DEFAULT_TIMEOUT_SEC = 30


def initialize_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    return logger


def is_file(path):
    if not validators.url(path):
        return PurePath(path).suffix != ""
    else:
        return False


def is_folder(path):
    if not validators.url(path):
        return not is_file(path)
    else:
        return False


def upload_file_with_pbar(src, dst):
    file_size = os.path.getsize(src)
    with open(src, "rb") as fd:
        with tqdm(
            desc=f"Uploading", total=file_size, unit="B",
            unit_scale=True, unit_divisor=1024
        ) as t:
            reader_wrapper = CallbackIOWrapper(t.update, fd, "read")
            response = requests.put(
                dst, data=reader_wrapper, timeout=DEFAULT_TIMEOUT_SEC
            )
            response.raise_for_status()


def upload_file_no_pbar(src, dst):
    with open(src, "rb") as fd:
        response = requests.put(dst, data=fd, timeout=DEFAULT_TIMEOUT_SEC)
        response.raise_for_status()

def upload_file(src, dst, pbar=False):
    if pbar:
        upload_file_with_pbar(src, dst)
    else:
        upload_file_no_pbar(src, dst)


def download_file_with_pbar(src, dst, chunk_size=DEFAULT_CHUNK_SIZE):
    response = requests.get(src, stream=True, timeout=DEFAULT_TIMEOUT_SEC)
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


def download_file_no_pbar(src, dst):
    with requests.get(
        src, stream=True, timeout=DEFAULT_TIMEOUT_SEC
    ) as response:
        response.raise_for_status()
        with open(dst, 'wb') as f:
            shutil.copyfileobj(response.raw, f)


def download_file(src, dst, chunk_size=DEFAULT_CHUNK_SIZE, pbar=False):
    if pbar:
        download_file_with_pbar(src, dst, chunk_size)
    else:
        download_file_no_pbar(src, dst)
