import logging
import json
import os
import requests
from datetime import datetime, date, timedelta
from base64 import b64encode
from statistics import stdev
from urllib import request
from urllib.parse import urlencode
from urllib3.exceptions import HTTPError

class APIAuthException(Exception):
    pass

logging.basicConfig(level=logging.DEBUG)
logging.getLogger(__name__)


class Settleboard:

    def __init__(self, auth):
        self.api_url = "https://settleboard-api.herokuapp.com"
        self.auth_header = auth

    def _api_request(self, endpoint, params=None):
        """ helper to do API GET calls """
        
        if params:
            response = requests.get(url=f"{self.api_url}/{endpoint}", headers={"Authorization":self.auth_header},
                                    params=params)
        else:
            response = requests.get(url=f"{self.api_url}/{endpoint}", headers={"Authorization":self.auth_header})
        code = response.status_code
        if 200 <= code < 300:
            logging.debug(f"API call: {self.api_url}/{endpoint} | {code}")
            encoding = response.encoding
            raw = response.content
            return json.loads(raw.decode(encoding))
        elif code > 500:
            raise APIAuthException
        else:
            logging.error(f"ERROR: Bad API call: {self.api_url}/{endpoint} | {code}")

    def _api_request_post(self, endpoint, data, headers=None):
        """ helper to do API POST calls """

        all_headers = {"Authorization": self.auth_header}

        if headers:
            for header in headers:
                all_headers[header] = headers[header]

        response = requests.post(url=f"{self.api_url}/{endpoint}", headers=all_headers, data=data)
        code = response.status_code
        if 200 <= code < 300:
            logging.debug(f"API POST call: {self.api_url}/{endpoint} | {code}")
            encoding = response.encoding
            raw = response.content
            return json.loads(raw.decode(encoding))
        elif code > 500:
            raise APIAuthException
        else:
            logging.error(f"ERROR: Bad API POST call: {self.api_url}/{endpoint} | {code}")

    def get_users(self):
        # GET https://settleboard-api.herokuapp.com/users
  
        response = self._api_request("users")
        if response is not None and response != []:
            return response

    def get_user_id(self, name):

        users = self.get_users()
        for user in users:
            if user['displayName'] == name:
                return user['id']
        return "No user by that name in database"

    def has_user(self, user):
        # GET https://settleboard-api.herokuapp.com/users/exists
        # return True if user is in database

        params = {"displayName": user}
        response = self._api_request("users/exists", params=params)
        if response is not None and response != []:
            return response['exists']

    def get_leaderboard(self):
        
        params={"offset": "0", "size": "10"}
        response = self._api_request("leaderboard", params=params)
        if response is not None and response != []:
            return response

    def get_last_user_match(self, user):
        """ get the last match a user participated in """

        user_id = self.get_user_id(user)
        endpoint = f"users/{user_id}/recent"
        response = self._api_request(endpoint)
        if response is not None and response != []:
            return response

    def create_match(self, p1, s1, p2, s2, p3, s3, p4=None, s4=None):

        id1 = self.get_user_id(p1)
        id2 = self.get_user_id(p2)
        id3 = self.get_user_id(p3)
        id4 = self.get_user_id(p4)

        headers = {"Content-Type": "application/json"}
        if p4:
            data = json.dumps({
                "scores": {
                    id1: s1,
                    id2: s2,
                    id3: s3,
                    id4: s4,
                }            
            })
        else:
            data = json.dumps({
                "scores": {
                    id1: s1,
                    id2: s2,
                    id3: s3,
                }
            })
        response = self._api_request_post("matches/", data, headers=headers)
        return response

    def make_user(self, name, password):
        """ create a new user """

        data = json.dumps({"password": password, "displayName": name})
        headers = {"Content-Type": "application/json"}
        response = self._api_request_post("users/", data, headers=headers)
        if response is not None and response != []:
            return response

    def authenticate_user(self, name, password):

        data = json.dumps({"password": password, "displayName": name})
        headers = {"Content-Type": "application/json"}
        response = self._api_request_post("users/authenticate", data, headers=headers)
        if response is not None and response != []:
            return response
