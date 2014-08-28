import requests
from helpers.error import ImgurClientError

API_URL = 'https://api.imgur.com/'


class AuthWrapper:
    def __init__(self, access_token, refresh_token, client_id, client_secret):
        self.current_access_token = access_token

        if refresh_token is None:
            raise TypeError('A refresh token must be provided')

        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret

    def get_refresh_token(self):
        return self.refresh_token

    def get_current_access_token(self):
        return self.current_access_token

    def refresh(self):
        data = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }

        url = API_URL + 'oauth2/token'

        response = requests.post(url, data=data)

        if response.status_code != 200:
            raise ImgurClientError('Error refreshing access token!', response.status_code)

        response_data = response.json()
        self.current_access_token = response_data['access_token']


class ImgurClient:

    def __init__(self, client_id=None, client_secret=None, access_token=None, refresh_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = None

        if refresh_token is not None:
            self.auth = AuthWrapper(access_token, refresh_token, client_id, client_secret)

    def get_client_id(self):
        return self.client_id

    def prepare_headers(self):
        if self.auth is None:
            if self.client_id is None:
                raise ImgurClientError('Client credentials not found!')
            else:
                return {'Authorization': 'Client-ID %s' % self.get_client_id()}
        else:
            return {'Authorization': 'Bearer %s' % self.auth.get_current_access_token()}

    def make_request(self, method, route, data=None):
        method = method.lower()
        method_to_call = getattr(requests, method)

        header = self.prepare_headers()
        url = API_URL + '3/%s' % route

        response = method_to_call(url, headers=header, data=data)

        if response.status_code == 403 and self.auth is not None:
            self.auth.refresh()
            header = self.prepare_headers()
            response = method_to_call(url, headers=header, data=data)

        try:
            response_data = response.json()

            if 'data' in response_data and 'error' in response_data['data']:
                raise ImgurClientError(response_data['data'], response.status_code)
        except:
            raise ImgurClientError('JSON decoding of response failed.')

        return response_data['data']