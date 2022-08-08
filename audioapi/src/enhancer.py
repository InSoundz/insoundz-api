import time
import wget
import validators
from pathlib import Path, PurePath
from halo import Halo
from audioapi.helpers import *
from audioapi.api import AudioAPI

DEFAULT_STATUS_INTERVAL_SEC = 0.5


class AudioEnhancer(object):
    """
    A wrapper for the audioapi client to produce audio enhancement.
    """
    def __init__(
        self,
        api_token,
        endpoint_url=AudioAPI.get_default_endpoint_url()
    ):
        self._logger = initialize_logger("AudioEnhancer")

        kwargs = dict(
            api_token=api_token,
            endpoint_url=endpoint_url,
            logger=self._logger,
        )
        kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
        self._api = AudioAPI(**kwargsNotNone)

    def _progress_text(self, start_time, sid, status):
        sec_counter = int(time.time() - start_time)
        return f"Session ID [{sid}]; Job status [{status}]; Elapsed time [{sec_counter} sec]  "

    def _update_job_done(self, sid, prev_status, status, pbar, spinner):
        if pbar and prev_status:
            if status == "failure":
                spinner.fail()
            else:
                spinner.succeed()
        else:
            self._logger.info(f"[{sid}] Job status [{status}]")

    def _handle_enhance_failure(self, sid, msg, status, pbar, spinner):
        if pbar:
            if status == "downloading" or status == "processing":
                spinner.fail()
            else:
                spinner.stop()

        self._logger.error(f"[{sid}] Failure reason: {msg}")

    def _get_default_dst_folder(self):
        return Path.cwd()

    def _get_default_dst_filename(self, src):
        src_filename = wget.detect_filename(src)
        src_filename_no_suffix = PurePath(src_filename).stem
        src_filename_suffix = PurePath(src_filename).suffix
        return src_filename_no_suffix + "_enhanced" + src_filename_suffix

    def _download_enhanced_file(self, sid, url, src, dst, pbar):
        if dst:
            # <dst> includes the full path (including the filename)
            if is_file(dst):
                folder = PurePath(dst).parent
                filename = PurePath(dst).name

            # <dst> includes only the directory (without the filename)
            elif is_folder(dst):
                folder = dst
                filename = self._get_default_dst_filename(src)

        # Use default path for download
        else:
            folder = self._get_default_dst_folder()
            filename = self._get_default_dst_filename(src)

        Path(folder).mkdir(parents=True, exist_ok=True)
        dst_path = os.path.join(folder, filename)

        self._logger.info(f"[{sid}] Downloading enhanced file to {dst_path}")
        download_file(url, str(dst_path), pbar)
        self._logger.info(f"[{sid}] {dst_path} was downloaded succesfully.")

    def _handle_enhance_done(self, sid, url, src, no_download, dst, pbar):
        self._logger.info(f"[{sid}] Enhanced file URL is located at {url}")
        if dst and validators.url(dst):
            self._logger.warning(f"[{sid}] Invalid destination path {dst}")
            dst = None

        # Downloading enhanced file
        if not no_download:
            self._download_enhanced_file(sid, url, src, dst, pbar)

    def _wait_till_done(self, sid, status_interval_sec, pbar, spinner):
        try:
            prev_status = None
            status = None
            while not time.sleep(status_interval_sec):
                response = self._api.enhance_status(sid)
                status = response["status"]

                if status != prev_status:
                    self._update_job_done(sid, prev_status, status, pbar, spinner)
                    start_time = time.time()

                if status == "done" or status == "failure":
                    return status, response

                if pbar:
                    spinner.start(text=self._progress_text(start_time, sid, status))
                prev_status = status

        except Exception as e:
            self._handle_enhance_failure(sid, e, status, pbar, spinner)
            raise

    def _enhancement_finish(
        self, sid, status, resp, src, no_download, dst, pbar, spinner
    ):
        if status == "done":
            url = resp["url"]
            self._logger.info(f"[{sid}] Enhanced file URL is located at {url}")

            # Downloading enhanced file
            if not no_download:
                self._download_enhanced_file(sid, url, src, dst, pbar)

        elif status == "failure" and pbar:
            spinner.stop()
            msg = resp["msg"]
            self._logger.error(f"[{sid}] Failure reason: {msg}")

        else:
            self._logger.exception(f"[{sid}] Unexpected status {status}")

    def _enhancement_start(self, api, src, dst, retention, pbar):
        self._logger.info(f"Sending a request to AudioAPI to enhance {src}")

        if validators.url(src):
            raise Exception(f"Invalid source path {src}")

        if dst and validators.url(dst):
            raise Exception(f"Invalid destination path {dst}")

        response = api.enhance_file(retention)
        sid = response["session_id"]
        src_url = response["upload_url"]
        self._logger.info(f"[{sid}] Uploading {src} to AudioAPI for processing.")
        upload_file(src, src_url, pbar)

        return sid

    def enhance_file(
            self, src, no_download=False, dst=None, retention=None,
            status_interval_sec=DEFAULT_STATUS_INTERVAL_SEC,
            progress_bar=False
        ):
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
        :param int  status_interval_sec:    
                                    The client can set the frequency of querying
                                    the status of the audio enhancement process.
                                    (This param is optional)
        :param int  progress_bar:   The client can enable/disable the display of
                                    the audio enhancement progress bar.
                                    (This param is optional)
        :return:                    None
        :rtype:                     None
        """

        spinner = None
        if progress_bar:
            spinner = Halo(spinner='dots', color='magenta', placement='right')

        try:
            sid = None
            sid = self._enhancement_start(self._api, src, dst, retention, progress_bar)
            status, resp = self._wait_till_done(
                sid, status_interval_sec, progress_bar, spinner
            )
            self._enhancement_finish(
                sid, status, resp, src, no_download, dst, progress_bar, spinner
            )

        except KeyError as e:
            self._logger.error(f"[{sid}] invalid key {e}")

        except Exception as e:
            self._logger.error(f"[{sid}] {e}")

    @staticmethod
    def get_default_status_interval():
        return DEFAULT_STATUS_INTERVAL_SEC