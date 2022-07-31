import logging
import sys
import time
import wget
from urllib.parse import urlparse
from pathlib import Path, PurePath
from halo import Halo
from audioapi.api import AudioAPI

DEFAULT_STATUS_INTERVAL_SEC = 0.5


class AudioEnhancer(object):
    """
    A wrapper for the audioapi client to produce audio enhancement.
    """
    def __init__(
        self,
        api_token, endpoint_url=AudioAPI.get_default_endpoint_url(),
        status_interval_sec=DEFAULT_STATUS_INTERVAL_SEC
    ):
        self._logger = self._initialize_logger("AudioEnhancer")
        self._api_token = api_token
        self._endpoint_url = endpoint_url
        self._status_interval_sec = status_interval_sec
        self._spinner = Halo(spinner='dots', color='magenta', placement='right')

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

    def _update_job_done(self, prev_status, status):
        if prev_status:
            if status == "failure":
                self._spinner.fail()
            else:
                self._spinner.succeed()

    def _progress_text(self, session_id, status, start_time):
        sec_counter = int(time.time() - start_time)
        return f"Session ID [{session_id}]; job status [{status}]; elapsed time [{sec_counter} sec]  "

    @staticmethod
    def get_default_status_interval():
        return DEFAULT_STATUS_INTERVAL_SEC

    def _get_default_dst_folder(self):
        return Path.cwd()

    def _get_default_dst_filename(self, src):
        src_filename = wget.detect_filename(src)
        src_filename_no_suffix = PurePath(src_filename).stem
        src_filename_suffix = PurePath(src_filename).suffix
        return src_filename_no_suffix + "_enhanced" + src_filename_suffix

    def _download_enhanced_file(self, enhanced_file_url, src, dst):
        if dst:
            # <dst> includes the full path (including the filename)
            if self._is_file(dst):
                dir = PurePath(dst).parent
                filename = PurePath(dst).name

            # <dst> includes only the directory (without the filename)
            elif Path(dst).is_dir():
                dir = dst
                filename = self._get_default_dst_filename(src)

        # Use default path for download
        else:
            dir = self._get_default_dst_folder()
            filename = self._get_default_dst_filename(src)

        Path(dir).mkdir(parents=True, exist_ok=True)
        dst_path = PurePath.joinpath(dir, filename)

        self._logger.info(f"Downloading enhanced file to {dst_path}")
        wget.download(enhanced_file_url, str(dst_path))
        print()  # An aesthetic linebreak
        self._logger.info(f"{dst_path} was downloaded succesfully.")

    def _upload_enhanced_file(self, enhanced_file_url, dst):
        raise NotImplementedError(f"Uploading enhanced file to {dst} - yet not supported.")

    def _is_url(self, path):
        if path:
            return urlparse(path).scheme != ""
        else:
            return False

    def _is_file(self, path):
        if not self._is_url(path):
            return PurePath(path).suffix != ""
        else:
            return False

    def _handle_enhance_file_done(
        self, src, no_download, dst, enhanced_file_url
    ):
        self._spinner.stop()
        self._logger.info(f"Enhanced file URL is located at "
                           "{enhanced_file_url}")

        # Uploading enhanced file
        if self._is_url(dst):
            self._upload_enhanced_file(enhanced_file_url, dst)
            return

        # Downloading enhanced file
        if not no_download:
            self._download_enhanced_file(enhanced_file_url, src, dst)

    def _handle_enhance_file_failure(self, msg, response):
        self._logger.error(f"Failure reason: {msg}")
        response.raise_for_status()

    def _get_key_from_response(self, key, response):
        if key in response.json().keys():
            return response.json()[key]
        else:
            self._spinner.fail()
            self._handle_enhance_file_failure(response.json()["message"], response)
            raise f"Invalid key: {key}"

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
        api = AudioAPI(**kwargsNotNone)

        try:
            if self._is_url(src):
                src_url = src
            else:
                # Send to /enhance a request to upload.
                # The last should return a URL to upload to.
                raise NotImplementedError("/enhance request to upload yet not supported.")

            # Send original file to AudioAPI
            self._logger.info(f"Sending {src_url} to AudioAPI for processing.")
            response = api.enhance_file(src_url, retention)
            session_id = self._get_key_from_response("session_id", response)

            # Check status
            prev_status = None
            while not time.sleep(self._status_interval_sec):
                response = api.enhance_status(session_id)
                status = self._get_key_from_response("status", response)
                
                if status != prev_status:
                    self._update_job_done(prev_status, status)
                    start_time = time.time()              

                if status == "done":
                    url = self._get_key_from_response("url", response)
                    self._handle_enhance_file_done(src, no_download, dst, url)
                    break
                elif status == "failure":
                    msg = self._get_key_from_response("msg", response)
                    self._handle_enhance_file_failure(msg, response)
                    break

                self._spinner.start(
                    text=self._progress_text(session_id, status, start_time)
                )    

                prev_status = status

        except Exception as e:
            self._logger.error(e)
            self._spinner.stop()
