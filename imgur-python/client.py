import requests
from imgur.models.album import Album
from imgur.models.image import Image
from imgur.models.account import Account
from imgur.models.comment import Comment
from helpers.error import ImgurClientError
from imgur.models.gallery_album import GalleryAlbum
from imgur.models.gallery_image import GalleryImage
from imgur.models.account_settings import AccountSettings

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
    allowed_album_fields = {
        'ids', 'title', 'description', 'privacy', 'layout', 'cover'
    }

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

        if method == 'delete':
            response = method_to_call(url, headers=header, params=data)
        else:
            response = method_to_call(url, headers=header, data=data)

        if response.status_code == 403 and self.auth is not None:
            self.auth.refresh()
            header = self.prepare_headers()
            if method == 'delete':
                response = method_to_call(url, headers=header, params=data)
            else:
                response = method_to_call(url, headers=header, data=data)

        # TODO: Add rate-limit checks

        try:
            response_data = response.json()
        except:
            raise ImgurClientError('JSON decoding of response failed.')

        if isinstance(response_data['data'], dict) and 'error' in response_data['data']:
            raise ImgurClientError(response_data['data']['error'], response.status_code)

        return response_data['data']

    def validate_user_context(self, username):
        if username == 'me' and self.auth is None:
            raise ImgurClientError('\'me\' can only be used in the authenticated context.')

    def logged_in(self):
        if self.auth is None:
            raise ImgurClientError('Must be logged in to complete request.')

    @staticmethod
    def build_gallery_images_and_albums(items):
        result = []
        for item in items:
            if item['is_album']:
                result.append(GalleryAlbum(item))
            else:
                result.append(GalleryImage(item))

        return result

    # Account-related endpoints
    def get_account(self, username):
        self.validate_user_context(username)
        account_data = self.make_request('GET', 'account/%s' % username)

        return Account(
            account_data['id'],
            account_data['url'],
            account_data['bio'],
            account_data['reputation'],
            account_data['created'],
            account_data['pro_expiration'],
        )

    def get_gallery_favorites(self, username):
        self.validate_user_context(username)
        gallery_favorites = self.make_request('GET', 'account/%s/gallery_favorites' % username)

        return self.build_gallery_images_and_albums(gallery_favorites)

    def get_account_favorites(self, username):
        self.validate_user_context(username)
        favorites = self.make_request('GET', 'account/%s/favorites' % username)

        return self.build_gallery_images_and_albums(favorites)

    def get_account_submissions(self, username, page=0):
        self.validate_user_context(username)
        submissions = self.make_request('GET', 'account/%s/submissions/%d' % (username, page))

        return self.build_gallery_images_and_albums(submissions)

    def get_account_settings(self, username):
        self.logged_in()
        settings = self.make_request('GET', 'account/%s/settings' % username)

        return AccountSettings(
            settings['email'],
            settings['high_quality'],
            settings['public_images'],
            settings['album_privacy'],
            settings['pro_expiration'],
            settings['accepted_gallery_terms'],
            settings['active_emails'],
            settings['messaging_enabled'],
            settings['blocked_users']
        )

    def change_account_settings(self, username, fields):
        allowed_fields = {
            'bio', 'public_images', 'messaging_enabled', 'album_privacy', 'accepted_gallery_terms', 'username'
        }

        post_data = {setting: fields[setting] for setting in set(allowed_fields).intersection(fields.keys())}

        return self.make_request('POST', 'account/%s/settings' % username, post_data)

    def get_email_verification_status(self, username):
        self.logged_in()
        self.validate_user_context(username)
        return self.make_request('GET', 'account/%s/verifyemail' % username)

    def send_verification_email(self, username):
        self.logged_in()
        self.validate_user_context(username)
        return self.make_request('POST', 'account/%s/verifyemail' % username)

    def get_account_albums(self, username, page=0):
        self.validate_user_context(username)

        albums = self.make_request('GET', 'account/%s/albums/%d' % (username, page))
        return [Album(album) for album in albums]

    def get_account_album_ids(self, username, page=0):
        self.validate_user_context(username)
        return self.make_request('GET', 'account/%s/albums/ids/%d' %  (username, page))

    def get_account_album_count(self, username):
        self.validate_user_context(username)
        return self.make_request('GET', 'account/%s/albums/count' % username)

    def get_account_comments(self, username, sort='newest', page=0):
        self.validate_user_context(username)
        comments = self.make_request('GET', 'account/%s/comments/%s/%s' % (username, sort, page))

        return [Comment(comment) for comment in comments]

    def get_account_comment_ids(self, username, sort='newest', page=0):
        self.validate_user_context(username)
        return self.make_request('GET', 'account/%s/comments/ids/%s/%s' % (username, sort, page))

    def get_account_comment_count(self, username):
        self.validate_user_context(username)
        return self.make_request('GET', 'account/%s/comments/count' % username)

    def get_account_images(self, username, page=0):
        self.validate_user_context(username)
        images = self.make_request('GET', 'account/%s/images/%d' % (username, page))

        return [Image(image) for image in images]

    def get_account_image_ids(self, username, page=0):
        self.validate_user_context(username)
        return self.make_request('GET', 'account/%s/images/ids/%d' % (username, page))

    def get_account_images_count(self, username, page=0):
        self.validate_user_context(username)
        return self.make_request('GET', 'account/%s/images/ids/%d' % (username, page))

    def get_album(self, album_id):
        album = self.make_request('GET', 'album/%s' % album_id)
        return Album(album)

    def get_album_images(self, album_id):
        images = self.make_request('GET', 'album/%s/images' % album_id)
        return [Image(image) for image in images]

    def create_album(self, fields):
        post_data = {field: fields[field] for field in set(self.allowed_album_fields).intersection(fields.keys())}

        if 'ids' in post_data:
            self.logged_in()

        return self.make_request('POST', 'album', data=post_data)

    def update_album(self, album_id, fields):
        post_data = {field: fields[field] for field in set(self.allowed_album_fields).intersection(fields.keys())}

        if isinstance(post_data['ids'], list):
            post_data['ids'] = ','.join(post_data['ids'])

        return self.make_request('POST', 'album/%s' % album_id, data=post_data)

    def album_delete(self, album_id):
        return self.make_request('DELETE', 'album/%s' % album_id)

    def album_favorite(self, album_id):
        self.logged_in()
        return self.make_request('POST', 'album/%s/favorite' % album_id)

    def album_set_images(self, album_id, ids):
        if isinstance(ids, list):
            ids = ','.join(ids)

        return self.make_request('POST', 'album/%s/' % album_id, {'ids': ids})

    def album_add_images(self, album_id, ids):
        if isinstance(ids, list):
            ids = ','.join(ids)

        return self.make_request('POST', 'album/%s/add' % album_id, {'ids': ids})

    def album_remove_images(self, album_id, ids):
        if isinstance(ids, list):
            ids = ','.join(ids)

        return self.make_request('DELETE', 'album/%s/remove_images' % album_id, {'ids': ids})