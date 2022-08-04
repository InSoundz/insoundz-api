import requests
from urllib.parse import urlunsplit
import logging

DEFAULT_ENDPOINT_URL = "api.insoundz.io"
DEFAULT_ENHANCE_VERSION = "v1"


class AudioAPI(object):
    """
    A basic and a simple class implementation of an audioapi client
    to access InSoundz AudioAPI.
    """
    def __init__(
            self,
            api_token,
            endpoint_url=DEFAULT_ENDPOINT_URL,
            logger=None):
        self._api_token = api_token
        self._endpoint_url = endpoint_url
        self._logger = logger
        if not self._logger:
            self._logger = logging.getLogger(__class__.__name__)
            self._logger.addHandler(logging.NullHandler())
        self._headers = {
            "Authorization": self._api_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def get_default_endpoint_url():
        return DEFAULT_ENDPOINT_URL

    def enhance_file(self, retention=None, version=DEFAULT_ENHANCE_VERSION):
        """
        Request the Audio API for a URL to upload the original audio file.
        The function returns a Response object with a upload_url key and a
        session_id key (to be later used by the enhance_status function).

        :param str retention:   The client can request to maintain the URL
                                of the enhanced audio file.
                                for <retention> minutes.
                                (This param is optional)

        :return:                A Response object that include response.json()
                                with a <session_id> and <upload_url> keys.
        :rtype:                 A requests.Response object
        """
        url = urlunsplit(('https', self._endpoint_url, f'{version}/enhance', '', ''))

        data = {}
        if retention:
            data["retention"] = retention

        return requests.put(url, headers=self._headers, json=data)

    def enhance_status(self, session_id, version=DEFAULT_ENHANCE_VERSION):
        """
        Checks the status of the audio file that is under audio enhancement
        process (by sending a <session_id> which was given by enhance_file()).

        :param str session_id:  Was given by enhance_file().
        :return:                A Response object that include 
                                response.json() with the keys:
                                #   <url> of the enhanced file in-case of
                                    <status> is "done".
                                #   <msg> in-case of
                                    <status> is "failure".
                                #   <status> only
                                    (of "downloading"|"processing").
        :rtype:                 A requests.Response object 
        """
        url = urlunsplit(('https', self._endpoint_url,
                         f'{version}/enhance/{session_id}', '', ''))

        return requests.get(url, headers=self._headers)
