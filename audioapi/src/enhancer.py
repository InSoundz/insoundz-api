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
        endpoint_url=AudioAPI.get_default_endpoint_url(),
        progress_bar=False
    ):
        self._logger = initialize_logger("AudioEnhancer")
        self._session_logger = None
        self._progress_bar = progress_bar
        self._spinner = Halo(spinner='dots', color='magenta', placement='right')
        self._progress_bar = progress_bar

        kwargs = dict(
            api_token=api_token,
            endpoint_url=endpoint_url,
            logger=self._logger,
        )
        kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
        self._api = AudioAPI(**kwargsNotNone)

    def _progress_text(self, start_time, session_id, status):
        sec_counter = int(time.time() - start_time)
        return f"Session ID [{session_id}]; Job status [{status}]; Elapsed time [{sec_counter} sec]  "

    def _start_spinner(self, start_time, session_id, status):
        if self._progress_bar:
            self._spinner.start(text=self._progress_text(start_time, session_id, status))

    def _update_job_done(self, prev_status, status):
        if self._progress_bar:
            if prev_status:
                if status == "failure":
                    self._spinner.fail()
                else:
                    self._spinner.succeed()
        else:
            self._session_logger.info(f"Job status [{status}]")

    def _handle_enhance_failure(self, msg, status):
        if self._progress_bar:
            if status == "downloading" or status == "processing":
                self._spinner.fail()
            else:
                self._spinner.stop()

        self._session_logger.error(f"Failure reason: {msg}")

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

        self._session_logger.info(f"Downloading enhanced file to {dst_path}")
        download_file(enhanced_file_url, str(dst_path), self._progress_bar)
        self._session_logger.info(f"{dst_path} was downloaded succesfully.")

    def _handle_enhance_done(self, enhanced_file_url, src, no_download, dst):
        self._session_logger.info(f"Enhanced file URL is located at "
                          f"{enhanced_file_url}")
        if dst and validators.url(dst):
            self._session_logger.warning(f"Invalid destination path {dst}")
            dst = None

        # Downloading enhanced file
        if not no_download:
            self._download_enhanced_file(enhanced_file_url, src, dst)

    def _wait_till_done(self, session_id, status_interval_sec):
        try:
            prev_status = None
            status = None
            while not time.sleep(status_interval_sec):
                response = self._api.enhance_status(session_id)
                status = get_key_from_dict("status", response)

                if status != prev_status:
                    self._update_job_done(prev_status, status)
                    start_time = time.time()

                if status == "done" or status == "failure":
                    return status, response

                self._start_spinner(start_time, session_id, status)
                prev_status = status

        except Exception as e:
            self._handle_enhance_failure(e, status)
            raise Exception(e)

    def _handle_job_done(self, status, response, src, no_download, dst):
        if status == "done":
            url = get_key_from_dict("url", response)
            self._handle_enhance_done(url, src, no_download, dst)
        elif status == "failure":
            msg = get_key_from_dict("msg", response)
            self._handle_enhance_failure(msg, status)
        else:
            self._session_logger.exception(f"Unexpected status {status}")

    def _handle_general_failure(self, msg):
        if self._session_logger:
            self._session_logger.error(msg)
        else:
            self._logger.error(msg)

    def _enhancement_start(self, api, src, retention):
        self._logger.info(f"Sending a request to AudioAPI to enhance {src}")

        if validators.url(src):
            raise Exception(f"Invalid source path {src}")

        response = api.enhance_file(retention)
        session_id = get_key_from_dict("session_id", response)
        src_url = get_key_from_dict("upload_url", response)
        self._session_logger = initialize_logger(f"AudioEnhancer [{session_id}]")
        self._session_logger.info(f"Uploading {src} to AudioAPI for processing.")
        upload_file(src, src_url, self._progress_bar)

        return session_id

    def enhance_file(
            self, src, no_download=False, dst=None, retention=None,
            status_interval_sec=DEFAULT_STATUS_INTERVAL_SEC
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
        :return:                    None
        :rtype:                     None
        """

        try:
            session_id = self._enhancement_start(self._api, src, retention)
            status, resp = self._wait_till_done(session_id, status_interval_sec)
            self._handle_job_done(status, resp, src, no_download, dst)

        except Exception as e:
            self._handle_general_failure(e)

    @staticmethod
    def get_default_status_interval():
        return DEFAULT_STATUS_INTERVAL_SEC