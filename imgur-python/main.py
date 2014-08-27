#!/usr/bin/env python3

import sys
import json
import math
from imgur.factory import Factory
from imgur.auth.expired import Expired
from helpers import format

try:
    from urllib.request import urlopen as urlllibopen
    from urllib.request import HTTPError
except ImportError:
    from urllib2 import urlopen as urlllibopen
    from urllib2 import HTTPError

authorized_commands = [
    'upload-auth',
    'comment',
    'vote-gallery',
    'vote-comment',
    'add-album-image'
]

oauth_commands = [
    'credits',
    'refresh',
    'authorize'
]

unauth_commands = [
    'upload',
    'list-comments',
    'get-album',
    'get-comment',
    'get-gallery'
]


def usage(argv):
    if len(argv) <= 1 or argv[1] == '--help' or argv[1] == '-h':
        print('\nUsage: \tpython main.py (action) [options...]')

        lines = []
        lines.append(('oauth', 'credits', 'View the rate limit information for this client'))
        lines.append(('oauth', 'authorize', 'Start the authorization process'))
        lines.append(('oauth', 'authorize [pin]', 'Get an access token after starting authorization'))
        lines.append(('oauth', 'refresh [refresh-token]', 'Return a new OAuth access token after it\'s expired'))

        lines.append(('anon', 'upload [file]', 'Anonymously upload a file'))
        lines.append(('anon', 'list-comments [hash]', 'Get the comments (raw JSON) for a gallery post'))
        lines.append(('anon', 'get-album [id]', 'Get information (raw JSON) about an album'))
        lines.append(('anon', 'get-comment [id]', 'Get a particular comment (raw JSON) for a gallery comment'))
        lines.append(('anon', 'get-gallery [hash]', 'Get information (raw JSON) about a gallery post'))

        lines.append(('auth', 'upload-auth [access-token]', 'Upload a file to your account'))
        lines.append(('auth', 'comment [access-token] [hash] [text ...]', 'Comment on a gallery post'))
        lines.append(('auth', 'vote-gallery [token] [hash] [direction]', 'Vote on a gallery post. Direction either \'up\', \'down\', or \'veto\''))
        lines.append(('auth', 'vote-comment [token] [id] [direction]', 'Vote on a gallery comment. Direction either \'up\', \'down\', or \'veto\''))
        lines.append(('auth', 'add-album-image [access-token] [album-id] [image-id]', 'Add an image to an album'))

        headers = {
            'oauth': 'OAuth Actions',
            'anon': 'Unauthorized Actions',
            'auth': 'Authorized Actions'
        }

        category_headers_output_so_far = []
        col_width = 0

        for category in headers.values():
            col_width = max(col_width, len(category))
        for line in lines:
            col_width = max(col_width, len(line[2]) + len(line[1]))

        col_width = math.ceil(col_width * 1.1)

        for line in lines:
            (cat, text, desc) = line

            if not cat in category_headers_output_so_far:
                print('\n' + format.center_pad(headers[cat], col_width) + '\n')
                category_headers_output_so_far.append(cat)
            print(format.two_column_with_period(text, desc, col_width) + '\n')

        sys.exit(1)


def main():
    usage(sys.argv)

    try:
        fd = open('data/config.json', 'r')
    except IOError:
        print('Config file [config.json] not found.')
        sys.exit(1)

    try:
        config = json.loads(fd.read())
    except ValueError:
        print('Invalid JSON in config file.')
        sys.exit(1)

    mfactory = Factory(config)
    action = sys.argv[1]

    if action in authorized_commands:
        handle_authorized_commands(mfactory, action)
    elif action in oauth_commands:
        handle_oauth_commands(mfactory, config, action)
    elif action in unauth_commands:
        handle_unauthorized_commands(mfactory, action)
    else:
        print('Invalid command provided! Use --help to see all available actions.')


def handle_authorized_commands(factory, action):
    token = sys.argv[2]
    auth = Factory.build_oauth(token, None)
    imgur = factory.build_api(auth)

    if action == 'upload-auth':
        path = sys.argv[3]
        req = factory.build_request_upload_from_path(path)
    elif action == 'comment':
        item_hash = sys.argv[3]
        text = ' '.join(sys.argv[4:])

        if len(text) > 140:
            print('Comment too long (trim by %d characters).' % (len(text) - 140))
            sys.exit(1)

        req = factory.build_request(('gallery', item_hash, 'comment'), {
            'comment': text
        })
    elif action == 'add-album-image':
        album_id = sys.argv[3]
        image_ids = ','.join(sys.argv[4:])

        req = factory.build_request(('album', album_id), {
            'ids[]': image_ids
        }, 'PUT')

    elif action in ('vote-gallery', 'vote-comment'):
        (target_id, vote) = sys.argv[3:]

        if action == 'vote-gallery':
            target = ('gallery', target_id, 'vote', vote)
        else:
            target = ('comment', target_id, 'vote', vote)

        req = factory.build_request(target, "")

    try:
        res = imgur.retrieve(req)

        if action == 'upload-auth':
            print(res['link'])
        else: 
            if action == 'comment':
                print('Success! https://www.imgur.com/gallery/%s/comment/%s' % (item_hash, res['id']))
            else:
                print(res)
    except Expired:
        print('Expired access token')


def handle_oauth_commands(factory, config, action):
    imgur = factory.build_api()

    if action == 'credits':
        req = factory.build_request(('credits',))
        res = imgur.retrieve(req)
        print(res)
    elif action == 'refresh':
        token = sys.argv[2]
        req = factory.build_request_oauth_refresh(token)

        try:
            res = imgur.retrieve_raw(req)
        except HTTPError as e:
            print('Error %d\n%s' % (e.code, e.read().decode('utf8')))
            raise e

        print('Access Token: %s\nRefresh Token: %s\nExpires: %d seconds from now.' % (
            res[1]['access_token'],
            res[1]['refresh_token'],
            res[1]['expires_in']
        ))
    elif action == 'authorize':
        if len(sys.argv) == 2:
            print('Visit this URL to get a PIN to authorize: %soauth2/authorize?client_id=%s&response_type=pin' % (
                factory.get_api_url(),
                config['client_id']
            ))
        if len(sys.argv) == 3:
            pin = sys.argv[2]
            imgur = factory.build_api()
            req = factory.build_request_oauth_token_swap('pin', pin)

            try:
                res = imgur.retrieve_raw(req)
            except HTTPError as e:
                print('Error %d\n%s' % (e.code, e.read().decode('utf8')))
                raise e
                
            print('Access Token: %s\nRefresh Token: %s\nExpires: %d seconds from now.' % (
                res[1]['access_token'],
                res[1]['refresh_token'],
                res[1]['expires_in']
            ))


def handle_unauthorized_commands(factory, action):
    imgur = factory.build_api()

    if action == 'upload':
        req = factory.build_request_upload_from_path(sys.argv[2])
        res = imgur.retrieve(req)

        print(res['link'])
    else:
        if action == 'list-comments':
            item_hash = sys.argv[2]
            req = factory.build_request(('gallery', item_hash, 'comments'))

        if action == 'get-album':
            id = sys.argv[2]
            req = factory.build_request(('album', id))

        if action == 'get-comment':
            cid = sys.argv[2]
            req = factory.build_request(('comment', cid))

        if action == 'get-gallery':
            id = sys.argv[2]
            req = factory.build_request(('gallery', id))

        res = imgur.retrieve(req)
        print(res)


if __name__ == "__main__":
    main()
