import requests
from http import HTTPStatus
from urllib.parse import urlencode, urlunsplit
import websockets
import logging

DEFAULT_API_ENDPOINT = "api.insoundz.io"


class AudioAPI(object):
    def __init__(
            self,
            api_token,
            api_endpoint=DEFAULT_API_ENDPOINT,
            logger=None):
        self._api_token = api_token
        self._api_endpoint = api_endpoint
        self._logger = logger
        if not self._logger:
            self._logger = logging.getLogger(__class__.__name__)
            self._logger.addHandler(logging.NullHandler())
        self._headers = {
            "Authorization": self._api_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _parse_response(self, response):
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            response.raise_for_status()

    @staticmethod
    def get_default_api_endpoint():
        return DEFAULT_API_ENDPOINT

    def enhance_file(self, file_url, retention=None):
        """
        Send a URL of the original audio file to the Audio API for audio
        enhancement. The function returns a JSON object with a sessionId key
        to be later used by the enhance_status function.

        :param str file_url:    The URL of the original audio file for
                                audio enhancement.
        :param str retention:   The client can request to maintain the URL
                                of the enhanced audio file.
                                for <retention> minutes.
                                (This param is optional)
        :return:                A JSON with a <sessionId>
        :rtype:                 A JSON object
        """
        url = urlunsplit(("https", self._api_endpoint, "enhance", "", ""))
        data = {"file_url": file_url}
        if retention:
            data["retention"] = retention

        response = requests.post(url, headers=self._headers, json=data)
        return self._parse_response(response)

    def enhance_status(self, session_id):
        """
        Checks the status of the audio file that is under audio enhancement
        process (by sending a <session_id> which was given by enhance_file()).

        :param str session_id:  Was given by enhance_file().
        :return:                A JSON with:
                                #   <url> of the enhanced file in-case of
                                    <status> is "done".
                                #   <msg> in-case of
                                    <status> is "failure".
                                #   <status> only
                                    (of "downloading"|"processing").
        :rtype:                 A JSON object
        """
        url = urlunsplit(('https', self._api_endpoint,
                         f'enhance/{session_id}', '', ''))

        response = requests.get(url, headers=self._headers)
        return self._parse_response(response)

    def enhance_websocket(self, sample_rate, file_type):
        """
        Returns a websocket connection.

        :param str sample_rate: Sample rate of the original file or stream
                                (measured in [hz]).
        :param str file_type:   Should be the file type ('wav', 'mp3' etc).
        :return:                A websocket connection.
        :rtype:                 A websocket connection object
        """
        parameters = {"sampleRate": sample_rate, "fileType": file_type}
        query = urlencode(query=parameters, doseq=True)
        uri = urlunsplit(("wss", self._api_endpoint, "/enhance", query, ""))

        try:
            conn = websockets.connect(uri)
        except Exception as e:
            self._logger.exception(e)

        return conn
