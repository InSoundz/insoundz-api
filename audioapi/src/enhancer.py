import time
import wget
import validators
from pathlib import Path, PurePath
from halo import Halo
from audioapi.helpers import *
from audioapi.api import AudioAPI

DEFAULT_STATUS_INTERVAL_SEC = 0.5


class Session(object):
    def __init__(self, api, session_id, src, no_download, dst, progress_bar):
        self._api = api
        self._id = session_id
        self._src = src
        self._dst = dst
        self._no_download = no_download
        self._spinner = Halo(spinner='dots', color='magenta', placement='right')
        self._status = None
        self._logger = initialize_logger(f"AudioEnhancer [{session_id}]")
        self._progress_bar = progress_bar

    def _progress_text(self, start_time):
        sec_counter = int(time.time() - start_time)
        return f"Session ID [{self._id}]; Job status [{self._status}]; Elapsed time [{sec_counter} sec]  "

    def _start_spinner(self, start_time):
        self._spinner.start(text=self._progress_text(start_time))

    def _update_job_done(self, prev_status):
        if prev_status:
            if self._status == "failure":
                self._spinner.fail()
            else:
                self._spinner.succeed()

    def _handle_enhance_failure(self, msg):
        if self._status == "downloading" or self._status == "processing":
            self._spinner.fail()
        else:
            self._spinner.stop()

        self._logger.error(f"Failure reason: {msg}")

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
        dst_path = PurePath.joinpath(folder, filename)

        self._logger.info(f"Downloading enhanced file to {dst_path}")
        download_file(enhanced_file_url, str(dst_path), self._progress_bar)
        self._logger.info(f"{dst_path} was downloaded succesfully.")

    def _handle_enhance_done(self, enhanced_file_url):
        self._logger.info(f"Enhanced file URL is located at "
                          f"{enhanced_file_url}")
        if self._dst and validators.url(self._dst):
            self._logger.warning(f"Invalid destination path {self._dst}")
            self._dst = None

        # Downloading enhanced file
        if not self._no_download:
            self._download_enhanced_file(enhanced_file_url, self._src, self._dst)

    def get_id(self):
        return self._id

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def wait_till_done(self, status_interval_sec):
        try:
            prev_status = None
            while not time.sleep(status_interval_sec):
                response = self._api.enhance_status(self.get_id())
                status = get_key_from_dict("status", response)
                self.set_status(status)

                if self.get_status() != prev_status:
                    self._update_job_done(prev_status)
                    start_time = time.time()

                if self.get_status() == "done" or self.get_status() == "failure":
                    return self.get_status(), response

                self._start_spinner(start_time)
                prev_status = self.get_status()

        except Exception as e:
            self._handle_enhance_failure(e)
            raise Exception(e)

    def handle_job_done(self, response):
        if self.get_status() == "done":
            url = get_key_from_dict("url", response)
            self._handle_enhance_done(url)
        elif self.get_status() == "failure":
            msg = get_key_from_dict("msg", response)
            self._handle_enhance_failure(msg)
        else:
            self._logger.exception(f"Unexpected status {self.get_status()}")


class AudioEnhancer(object):
    """
    A wrapper for the audioapi client to produce audio enhancement.
    """
    def __init__(
        self,
        api_token,
        endpoint_url=AudioAPI.get_default_endpoint_url(),
        status_interval_sec=DEFAULT_STATUS_INTERVAL_SEC,
        progress_bar=False
    ):
        self._logger = initialize_logger("AudioEnhancer")
        self._status_interval_sec = status_interval_sec
        self._progress_bar = progress_bar
        self._sessions_list = {}

        kwargs = dict(
            api_token=api_token,
            endpoint_url=endpoint_url,
            logger=self._logger,
        )
        kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
        self._api = AudioAPI(**kwargsNotNone)

    def _create_session(self, api, session_id, src, no_download, dst):
        self._sessions_list[session_id] = Session(
                api, session_id, src, no_download, dst, self._progress_bar
            )
        return self._sessions_list[session_id]

    def _enhancement_start(self, api, src, no_download, dst, retention):
        self._logger.info(f"Sending a request to AudioAPI to enhance {src}")

        if validators.url(src):
            raise Exception(f"Invalid source path {src}")

        response = api.enhance_file(retention)
        session_id = get_key_from_dict("session_id", response)
        src_url = get_key_from_dict("upload_url", response)
        self._logger.info(f"Uploading {src} to AudioAPI for processing.")
        upload_file(src, src_url, self._progress_bar)

        session = self._create_session(api, session_id, src, no_download, dst)
        return session

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

        session = None

        try: 
            session = self._enhancement_start(self._api, src, no_download, dst, retention)
            _, resp = session.wait_till_done(self._status_interval_sec)
            session.handle_job_done(resp)

        except Exception as e:
            self._logger.error(e)

        finally:
            if session and session.get_id() in self._sessions_list:
                del self._sessions_list[session.get_id()]

    @staticmethod
    def get_default_status_interval():
        return DEFAULT_STATUS_INTERVAL_SEC