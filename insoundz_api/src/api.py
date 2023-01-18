import requests
from urllib.parse import urlunsplit
import logging

DEFAULT_ENDPOINT_URL = "api.insoundz.io"
DEFAULT_ENHANCE_VERSION = "v1"
DEFAULT_TIMEOUT_SEC = 30


class insoundzAPI(object):
    """
    A basic and simple class implementation of insoundz API client.
    """
    def __init__(
            self,
            client_id,
            secret,
            endpoint_url=DEFAULT_ENDPOINT_URL,
            logger=None):
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self._endpoint_url = endpoint_url
        auth_token, _ = self.account_token(client_id, secret)
        self.set_auth_token(auth_token)

        self._logger = logger
        if not self._logger:
            self._logger = logging.getLogger(__class__.__name__)
            self._logger.addHandler(logging.NullHandler())

    def set_auth_token(self, auth_token):
        self._auth_token = auth_token
        self._headers.update({"Authorization": auth_token})

    def account_token(
        self, client_id, secret, version=DEFAULT_ENHANCE_VERSION
    ):
        """
        Based on client_id and secret from the User Management System,
        retrieve an JWT Token
        """
        url = urlunsplit(
            ('https', self._endpoint_url,
            f'{version}/account/token', '', '')
        )

        data = {
            "client_id": client_id,
            "secret": secret
        }

        response = requests.post(
            url, headers=self._headers, json=data, timeout=DEFAULT_TIMEOUT_SEC
        )

        response.raise_for_status()

        response = response.json()
        token = response["token"]
        expires = response["expires"]

        return token, expires

    @staticmethod
    def get_default_endpoint_url():
        return DEFAULT_ENDPOINT_URL

    def enhance_file(self, retention=None, preset=None, version=DEFAULT_ENHANCE_VERSION):
        """
        Request the Audio API for a URL to upload the original audio file.
        The function returns an upload_url and a session_id
        (to be later used by the enhance_status function).

        :param str retention:   The client can request to maintain the URL
                                of the enhanced audio file.
                                for <retention> minutes.
                                (This param is optional)

        :param str preset:      The desired postprocessing preset for the 
                                file in question. The avalible presets are
                                'flat' and 'post'.

        :return:                A <session_id> and an <upload_url>.
        :rtype:                 Tuple
        """
        url = urlunsplit(
            ('https', self._endpoint_url,
            f'{version}/enhance', '', '')
        )

        data = {}
        if retention:
            data["retention"] = retention
        
        if preset:
            data["preset"] = preset

        response = requests.post(
            url, headers=self._headers, json=data, timeout=DEFAULT_TIMEOUT_SEC
        )

        response.raise_for_status()

        response = response.json()
        sid = response["session_id"]
        src_url = response["upload_url"]

        return sid, src_url

    def enhance_status(self, session_id, version=DEFAULT_ENHANCE_VERSION):
        """
        Checks the status of the audio file that is under audio enhancement
        process (by sending a <session_id> which was given by enhance_file()).
        The function returns the status and additional info.

        :param str session_id:  Was given by enhance_file().
        :return:                A <status> and <resp_info>.
                                #   <resp_info> will contain a url of the
                                    enhanced file in-case of <status> is "done"
                                #   <resp_info> will contain the failure
                                    details in-case of <status> is "failure"
        :rtype:                 Tuple
        """
        url = urlunsplit(
            ('https', self._endpoint_url,
            f'{version}/enhance/{session_id}', '', '')
        )

        response = requests.get(
            url, headers=self._headers, timeout=DEFAULT_TIMEOUT_SEC
        )

        response.raise_for_status()

        response = response.json()
        status = response["status"]

        if status == "done":
            resp_info = response["url"]
        elif status == "failure":
            resp_info = response["msg"]
        else:
            resp_info = None

        return status, resp_info

    def balance(self, version=DEFAULT_ENHANCE_VERSION):
        """
        Based on client_id and secret from the User Management System,
        retrieve the client current balance.
        """
        url = urlunsplit(
            ('https', self._endpoint_url,
            f'{version}/account/balance', '', '')
        )

        response = requests.get(
            url, headers=self._headers, timeout=DEFAULT_TIMEOUT_SEC
        )

        response.raise_for_status()
        response = response.json()
        
        return response["balance"]

    def version(self, version=DEFAULT_ENHANCE_VERSION):
        """
        Retrieve insoundz API server version.
        """
        url = urlunsplit(
            ('https', self._endpoint_url,
            f'{version}/version', '', '')
        )

        response = requests.get(
            url, headers=self._headers, timeout=DEFAULT_TIMEOUT_SEC
        )

        response.raise_for_status()
        response = response.json()

        return response['version'], response['build']
