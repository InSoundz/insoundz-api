import time
import validators
import requests
from http import HTTPStatus
from pathlib import Path, PurePath
from halo import Halo
from insoundz_api.helpers import *
from insoundz_api.api import insoundzAPI

DEFAULT_STATUS_INTERVAL_SEC = 0.5
MAX_UNAUTHORIZED_RETRIES = 10


class AudioEnhancer(object):
    """
    A wrapper for insoundz API client to produce audio enhancement.
    """
    def __init__(
        self,
        client_id,
        secret,
        endpoint_url=insoundzAPI.get_default_endpoint_url()
    ):
        self._logger = initialize_logger("AudioEnhancer")

        kwargs = dict(
            client_id=client_id,
            secret=secret,
            endpoint_url=endpoint_url,
            logger=self._logger,
        )
        kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
        self._api = insoundzAPI(**kwargsNotNone)

    def _progress_text(self, start_time, sid, status):
        sec_counter = int(time.time() - start_time)
        return f"Session ID [{sid}]; Job status [{status}]; " \
            f"Elapsed time [{sec_counter} sec]  "

    def _update_status_changed(self, sid, prev_status, status, pbar, spinner):
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
        src_filename = os.path.basename(src)
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

        # Downloading enhanced file
        if not no_download:
            self._download_enhanced_file(sid, url, src, dst, pbar)

    def _wait_till_done(self, sid, status_interval_sec, pbar, spinner):    
        prev_status = None
        status = None
        retries = MAX_UNAUTHORIZED_RETRIES

        while not time.sleep(status_interval_sec):
            try:
                status, resp_info = self._api.enhance_status(sid)

                if status != prev_status:
                    self._update_status_changed(
                        sid, prev_status, status, pbar, spinner
                    )
                    start_time = time.time()

                if status == "done" or status == "failure":
                    return status, resp_info

                if pbar:
                    spinner.start(
                        text=self._progress_text(start_time, sid, status)
                    )
                prev_status = status

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == HTTPStatus.UNAUTHORIZED and retries:
                    retries -= 1
                else:
                    self._handle_enhance_failure(sid, e, status, pbar, spinner)
                    raise

            except Exception as e:
                self._handle_enhance_failure(sid, e, status, pbar, spinner)
                raise

            else:
                retries = MAX_UNAUTHORIZED_RETRIES

    def _enhancement_finish(
        self, sid, status, info, src, no_download, dst, pbar, spinner
    ):
        if status == "done":
            self._logger.info(
                f"[{sid}] Enhanced file URL is located at {info}"
            )

            # Downloading enhanced file
            if not no_download:
                self._download_enhanced_file(sid, info, src, dst, pbar)

        elif status == "failure" and pbar:
            spinner.stop()
            self._logger.error(f"[{sid}] Failure reason: {info}")

        else:
            self._logger.exception(f"[{sid}] Unexpected status {status}")

    def _enhancement_start(self, api, src, dst, retention, preset, pbar):
        self._logger.info(f"Sending a request to insoundzAPI to enhance {src}")

        if validators.url(src):
            raise Exception(f"Invalid source path {src}")

        if dst and validators.url(dst):
            raise Exception(f"Invalid destination path {dst}")

        sid, src_url = api.enhance_file(retention, preset)

        self._logger.info(
            f"[{sid}] Uploading {src} to insoundzAPI for processing."
        )
        upload_file(src, src_url, pbar)

        return sid

    def enhance_file(
        self, src, no_download=False, dst=None, retention=None,
        preset=None, status_interval_sec=DEFAULT_STATUS_INTERVAL_SEC,
        progress_bar=False
    ):
        """
        It uses insoundz_api package to enhance the file that is located
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
        :param int  retention:      The client can request insoundzAPI to keep
                                    the URL of the enhanced file alive for a
                                    <retention> minutes (retention time).
                                    Otherwise there is no guarantee for how
                                    long the URL will be available and
                                    therefore it's not recommanded to set the
                                    <no_download> flag.
                                    (This param is optional)
        :param str  preset:         The client can choose between 2 audio presets; 
                                    The 'flat' preset includes Denoising, Dereverbration, 
                                    Click sounds filtering and Deplosive. The 'post' preset 
                                    includes everything from 'flat' and Auto-Mixing, 
                                    Dynamic-EQ, Multi speaker leveling, Loudness correction..
        :param int  status_interval_sec:
                                    The client can set the frequency of
                                    querying the status of the audio
                                    enhancement process.
                                    (This param is optional)
        :param int  progress_bar:   The client can enable/disable the display
                                    of the audio enhancement progress bar.
                                    (This param is optional)
        :return:    sid:            The session ID.
                    status:         Enhancment final status ("done" or "failure")
                    resp_info:      Final status additinal info (Enhanced file url
                                    if status "done. Error message if status "failure".)
        :rtype:                     Tuple
        """

        spinner = None
        if progress_bar:
            spinner = Halo(spinner='dots', color='magenta', placement='right')

        sid = None
        status = None
        resp_info = None

        try:
            sid = self._enhancement_start(
                self._api, src, dst, retention, preset, progress_bar
            )
            status, resp_info = self._wait_till_done(
                sid, status_interval_sec, progress_bar, spinner
            )
            self._enhancement_finish(
                sid, status, resp_info, src,
                no_download, dst, progress_bar, spinner
            )

        except KeyError as e:
            self._logger.error(f"[{sid}] invalid key {e}")

        except Exception as e:
            self._logger.error(f"[{sid}] {e}")

        return sid, status, resp_info

    @staticmethod
    def get_default_status_interval():
        return DEFAULT_STATUS_INTERVAL_SEC
