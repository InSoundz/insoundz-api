import logging
import sys
import time
import wget
import os
from urllib.parse import urlparse
from pathlib import Path
from audioapi import audioapi

DEFAULT_STATUS_INTERVAL_SEC = 1


class AudioEnhancer(object):
    def __init__(
        self,
        api_token, endpoint_url,
        status_interval_sec=DEFAULT_STATUS_INTERVAL_SEC
    ):
        self._logger = self._initialize_logger("AudioEnhancer")
        self._api_token = api_token
        self._endpoint_url = endpoint_url
        self._status_interval_sec = status_interval_sec

    def _initialize_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)
        return logger

    @staticmethod
    def get_default_status_interval():
        return DEFAULT_STATUS_INTERVAL_SEC

    def _get_default_dst_folder(self):
        return os.getcwd()

    def _get_default_dst_filename(self, src):
        src_filename_with_ext = os.path.split(src)[1]
        src_filename_not_ext = os.path.splitext(src_filename_with_ext)[0]
        src_filename_ext = os.path.splitext(src_filename_with_ext)[1]     
        return src_filename_not_ext + "_enhanced" + src_filename_ext

    def _download_enhanced_file(self, enhanced_file_url, dst):
        self._logger.info(f"Downloading enhanced file to {dst}")
        wget.download(enhanced_file_url, dst)
        print()  # An aesthetic linebreak
        self._logger.info(f"{dst} was downloaded succesfully.")

    def _upload_enhanced_file(self, enhanced_file_url, dst):
        raise NotImplementedError(f"Uploading enhanced file to {dst} - yet not supported.")

    def _is_url(self, path):
        if path:
            return urlparse(path).scheme != ""
        else:
            return False 

    def _is_file(self, path):
        if path:
            return os.path.splitext(path)[1] != ""
        else:
            return False 

    def _is_folder(self, path):
        if path:
            return not self._is_file(path)
        else:
            return False 

    def enhance_file(self, src, no_download=False, dst=None, retention=None):
        """
        It uses the audioapi package to enhance the file that is located
        in <src>.
        After the audio enhancement process is done, the URL of the new and
        enhanced file will be displayed.
        If <dst> is a URL, the enhanced file will be uploaded to this URL.
        If <dst> is a file or directory path, the enhanced file will be
        downloaded to the local machine (unless the <no_download> flag is set).

        :param str  src:            Contains a URL or a local path of the
                                    original audio file.
        :param bool no_download:    Set this flag if want to skip the download
                                    of the enhanced file to the local machine.
                                    (This param is optional)
        :param str  dst:            If <dst> is a URL, the enhanced file will
                                    be uploaded to this URL.
                                    If <dst> is a file or directory path, the
                                    enhanced file will be downloaded to the
                                    local machine (unless the <no_download>
                                    flag is set).
                                    If <dst> is missing, the enhanced file
                                    will be downloaded to the current directory
                                    under the name
                                    <original_filename>_enhanced.wav (unless
                                    the <no_download> flag is set).
                                    (This param is optional)
        :param int  retention:      The client can request the audioapi to keep
                                    the URL of the enhanced file alive for a
                                    <retention> minutes (retention time).
                                    Otherwise there is no guarantee for how
                                    long the URL will be available and
                                    therefore it's not recommanded to set the
                                    <no_download> flag.
                                    (This param is optional)
        :return:                    None
        :rtype:                     None
        """

        kwargs = dict(
            api_token=self._api_token,
            endpoint_url=self._endpoint_url,
            logger=self._logger,
        )
        kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
        api = audioapi.AudioAPI(**kwargsNotNone)

        try:
            if self._is_url(src):
                src_url = src
            else:
                # Send to /enhance a request to upload.
                # The last should return a URL to upload to.
                raise NotImplementedError("/enhance request to upload yet not supported.")

            # Send original file to AudioAPI
            self._logger.info(f"Sending {src_url} to AudioAPI for processing.")
            ret_val = api.enhance_file(src_url, retention)
            session_id = ret_val["session_id"]

            # Check status
            prev_status = None
            while True:
                ret_val = api.enhance_status(session_id)
                status = ret_val["status"]
                if status != prev_status:
                    self._logger.info(
                        f"Session ID [{session_id}] job status [{status}]."
                    )
                prev_status = status

                if status == "done":
                    enhanced_file_url = ret_val["url"]
                    self._logger.info(
                        f"Enhanced file URL is located at {enhanced_file_url}"
                    )
                    break
                elif status == "failure":
                    failure_reason = ret_val["msg"]
                    self._logger.error(f"Failure reason: {failure_reason}")
                    break
                else:
                    time.sleep(self._status_interval_sec)

            # Handle audio enhancement done
            if status == "done":
                
                # Uploading enhanced file
                if self._is_url(dst):
                    self._upload_enhanced_file(enhanced_file_url, dst)
                
                # Downloading enhanced file
                elif not no_download:
                    folder_path = None
                    file_name = None

                    # <dst> includes the full path (including the filename)
                    if self._is_file(dst):
                        folder_path = os.path.split(dst)[0]
                        file_name = os.path.split(dst)[1]
                    
                    # <dst> includes the path (without the filename)
                    elif self._is_folder(dst):
                        folder_path = dst
                        file_name = self._get_default_dst_filename(src)
                    
                    # <dst> is None, so we download to default path
                    else:
                        folder_path = self._get_default_dst_folder()
                        file_name = self._get_default_dst_filename(src)

                    Path(folder_path).mkdir(parents=True, exist_ok=True)
                    dst_path = os.path.join(folder_path, file_name)
                    self._download_enhanced_file(enhanced_file_url, dst_path)

        except Exception as e:
            self._logger.error(e)

    # TODO: need to support this use-case
    def enhance_stream(
            self, src_stream_type, src, dst, rate, chunksize):
        raise NotImplementedError("'enhance_stream()' yet not supported.")
