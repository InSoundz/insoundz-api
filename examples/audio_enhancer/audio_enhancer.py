import logging
import sys
import time
import wget
import boto3
import os
from audioapi import audioapi


# should be taken from audioapi module with get_backet() ?
BACKET = 'insoundz-wavs'
AUDIOAPI_UPLOAD_DIR = 'audioapi_tmp'
DEFAULT_STATUS_INTERVAL_SEC = 1


class AudioEnhancer(object):
    def __init__(self, api_token, api_endpoint, status_interval_sec = DEFAULT_STATUS_INTERVAL_SEC):
        self._logger = self._initialize_logger("AudioEnhancer")
        self._api_token = api_token
        self._api_endpoint = api_endpoint
        self._status_interval_sec = status_interval_sec

    def _initialize_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)
        return logger

    def _upload_src_file_to_s3(self, src_path):
        try:
            self._logger.info(f"Uploading {src_path}.")
            filename = os.path.split(src_path)[1]  # assuming a valid path (file with extension)
            key = os.path.join(AUDIOAPI_UPLOAD_DIR, filename)
            s3 = boto3.resource('s3')
            s3.meta.client.upload_file(src_path, BACKET, key)
            src_uri = os.path.join("s3://", BACKET, key)
        except Exception as e:
            self._logger.exception(e)

        self._logger.info(f"{src_path} was uploaded succesfully to {src_uri}.")
        return src_uri

    def _delete_file_from_s3(self, src_uri):
        try:
            self._logger.info(f"Deleting {src_uri}.")
            filename = os.path.split(src_uri)[1]
            key = os.path.join(AUDIOAPI_UPLOAD_DIR, filename)
            s3 = boto3.resource('s3')
            s3.Object(BACKET, key).delete()
        except Exception as e:
            self._logger.exception(e)

        self._logger.info(f"{src_uri} was deleted succesfully to {src_uri}.")

    def _create_dst_path(self, src_path):
        src_filename_with_ext = os.path.split(src_path)[1]
        src_filename_not_ext = os.path.splitext(src_filename_with_ext)[0]
        dst_path = os.path.join(os.getcwd(), src_filename_not_ext + "_enhanced.wav")
        return dst_path

    def _download_enhanced_file(self, enhanced_file_uri, dst_path):
        self._logger.info(f"Downloading enhanced file to local machine at {dst_path}")
        wget.download(enhanced_file_uri, dst_path)
        self._logger.info("")  # An aesthetic linebreak

    def enhance_file(self, src_type, src_path, no_download, dst_path, retention=None):
        """ 
        It uses the audioapi package to enhance the file that is located in <src_path>. 
        After the audio enhancement process is done, the URI of the new and enhanced file will be displayed.
        The enhanced file will be downloaded to the local machine at <dst_path> unless
        the <no_download> flag is set.

        :param str  src_type:       Should only be 'local' or 'remote'.
        :param str  src_path:       If <src_type=='local'> then <src_path> contain a full path of the original audio file on the local machine. 
                                    If <src_type=='remote'> then <src_path> contain the URI of the original audio file.
        :param bool no_download:    Set this flag if want to skip the download of the enhanced file to the local machine.
        :param str  dst_path:       The enhanced file will be downloaded to the local machine at <dst_path> unless
                                    the <no_download> flag is set.
                                    If <dst_path> is missing, the enhanced file will be downloaded to the current directory
                                    under the name <original_filename>_enhanced.wav.
        :param int  retention:      The client can request the audioapi to keep the URI of the enhanced file 
                                    alive for a <retention> minutes (retention time). Otherwise there is no
                                    guarantee for how long the URI will be available and therefore it's
                                    recommanded to use the download (so don't set the <no_download> flag).
                                    (This param is optional)
        :return:                    None
        :rtype:                     None
        """

        kwargs = dict(api_token=self._api_token, api_endpoint=self._api_endpoint, logger=self._logger)
        kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
        api = audioapi.AudioAPI(**kwargsNotNone)

        try:
            # Upload the local file to a temporary URI
            if src_type == 'local':
                src_uri = self._upload_src_file_to_s3(src_path)
            elif src_type =='remote':
                src_uri = src_path
            else:
                raise Exception("Illegal <src_type>. Must be 'local' or 'remote'.")

            # Send original file to AudioAPI
            self._logger.info(f"Sending {src_uri} to AudioAPI for processing.")
            ret_val = api.enhance_file(src_uri, retention)
            session_id = ret_val["sessionId"]

            # Check status
            prev_status = None
            while True:
                ret_val = api.enhance_status(session_id)
                status = ret_val["status"]
                if status != prev_status:
                    self._logger.info(f"Session ID [{session_id}] job status [{status}].")
                prev_status = status

                if status == "DONE":
                    enhanced_file_uri = ret_val["file_uri"]
                    self._logger.info(f"Enhanced file URI is located at {enhanced_file_uri}")
                    break
                elif status == "FAILURE":
                    failure_reason = ret_val["failure_reason"]
                    self._logger.error(f"Failure reason: {failure_reason}")
                    break
                else:
                    time.sleep(self._status_interval_sec)

            # Downloading enhanced file
            if status == "DONE" and not no_download:
                if not dst_path:
                    dst_path = self._create_dst_path(src_path)
                self._download_enhanced_file(enhanced_file_uri, dst_path)

            # Delete the original file URI in case it was created by the script
            if src_type == 'local':
                self._delete_file_from_s3(src_uri)

        except Exception as e:
            self._logger.error(e)

    # TODO: need to support this use-case
    def enhance_stream(self, src_stream_type, src_path, dst_path, rate, chunksize):
        raise NotImplementedError("'enhance_stream()' yet not supported.")
