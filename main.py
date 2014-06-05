#!/usr/bin/env python3
import json, sys, time as dt, pprint, math

from Imgur.Factory import Factory
from Imgur.Auth.Expired import Expired

try:
    from urllib.request import urlopen as UrlLibOpen
    from urllib.request import HTTPError
except ImportError:
    from urllib2 import urlopen as UrlLibOpen
    from urllib2 import HTTPError

def center_pad(s, length):
    num_dashes = float(length - len(s) - 2) / 2
    num_dashes_left = int(math.floor(num_dashes))
    num_dashes_right = int(math.ceil(num_dashes))

    return ('=' * num_dashes_left) + ' ' + s + ' ' + ('=' * num_dashes_right)

def two_column_with_period(left, right, length):
    num_periods = int(length - (len(left) + len(right) + 2))
    return left + ' ' + ('.' * num_periods) + ' ' + right

def usage(argv):
    if len(argv) <= 1 or argv[1] == '--help' or argv[1] == '-h':

        print("\nUsage: \tpython main.py (action) [options...]")

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

        headers = {
            'oauth': 'OAuth Actions',
            'anon': 'Unauthorized Actions',
            'auth': 'Authorized Actions'
        }

        categoryHeadersOutputSoFar = []
        
        col_width = 0
        for category in headers.values():
            col_width = max(col_width, len(category))
        for line in lines:
            col_width = max(col_width, len(line[2]) + len(line[1]))

        col_width = math.ceil(col_width * 1.1)

        for line in lines:
            (cat, text, desc) = line

            if False == (cat in categoryHeadersOutputSoFar):
                print("\n" + center_pad(headers[cat], col_width) + "\n")
                categoryHeadersOutputSoFar.append(cat)
            print(two_column_with_period(text, desc, col_width))

        print("")
        '''

        print("\n" + sep + "\nOAuth Actions\n" + sep)
        print("credits\n-- View the rate limit information for this client")
        print("authorize\n-- Get the authorization URL")
        print("authorize [pin]\n-- Get an access token")
        print("refresh [refresh-token]\n-- Return a new OAuth access token after it's expired")

        print("\n" + sep + "\nUnauthorized Actions\n" + sep)
        print("upload [file]\n-- Anonymously upload a file")
        print("list-comments [hash]\n-- Get the comments (raw json) for a gallery item")
        print("get-album [id]\n-- View information about an album")
        print("get-comment [id]\n-- Get a particular comment (raw json) for a gallery item")
        print("get-gallery [hash]\n-- View information about a gallery post")

        print("\n" + sep + "\nAuthorized Actions\n" + sep)
        print("upload-auth [access-token] [file]\n-- Upload a file to your account")
        print("comment [access-token] [hash] [text]\n-- Comment on a gallery image")
        print("vote-gallery [token] [hash] [direction]\n-- Vote on a gallery post. Direction either 'up', 'down', or 'veto'")
        print("vote-comment [token] [id] [direction]\n-- Vote on a gallery comment. Direction either 'up', 'down', or 'veto'")
        print("\n")
        '''

        sys.exit(1)

def main():
    usage(sys.argv)

    config = None
    try:
        fd = open('config.json', 'r')
    except:
        print("config file [config.json] not found.")
        sys.exit(1)

    try:
        config = json.loads(fd.read())
    except:
        print("invalid json in config file.")
        sys.exit(1)

    factory = Factory(config)


    action = sys.argv[1]

    authorized_commands = [
        'upload-auth',
        'comment',
        'vote-gallery',
        'vote-comment'
    ]

    oauth_commands = [
        'credits',
        'refresh',
        'authorize'
    ]

    if action in authorized_commands:
        handle_authorized_commands(factory, action)
    else:
        if action in oauth_commands:
            handle_oauth_commands(factory, config, action)
        else:
            handle_unauthorized_commands(factory, action)

def handle_authorized_commands(factory, action):
    token = sys.argv[2]
    auth = factory.build_oauth(token, None)
    imgur = factory.build_api(auth)

    if action == 'upload-auth':
        path = sys.argv[3]
        req = factory.build_request_upload_from_path(path)

    if action == 'comment':
        thash = sys.argv[3]
        text = ' '.join(sys.argv[4:])

        if len(text) > 140:
            print("Comment too long (trim by %d characters)." % (len(text) - 140))
            sys.exit(1)

        req = factory.build_request(('gallery', thash, 'comment'), {
            'comment': text
        })

    if action == 'vote-gallery' or action == 'vote-comment':
        (tid, vote) = sys.argv[3:]

        target = None
        if action == 'vote-gallery':
            target = ('gallery', tid, 'vote', vote)
        else:
            target = ('comment', tid, 'vote', vote)

        req = factory.build_request(target)

    try:
        res = imgur.retrieve(req)
        if action == 'upload-auth':
            print(res['link'])
        else: 
            if action == 'comment':
                print("Success! https://www.imgur.com/gallery/%s/comment/%s" % (thash, res['id']))
            else:
                print(res)
    except Expired:
        print("Expired access token")



def handle_oauth_commands(factory, config, action):
    imgur = factory.build_api()

    if action == 'credits':
        req = factory.build_request(('credits',))
        res = imgur.retrieve(req)
        print(res)

    if action == 'refresh':
        token = sys.argv[2]
        req = factory.build_request_oauth_refresh(token)

        try:
            res = imgur.retrieve_raw(req)
        except HTTPError as e:
            print("Error %d\n%s" % (e.code, e.read().decode('utf8')))
            raise e

        print('Access Token: %s\nRefresh Token: %s\nExpires: %d seconds from now.' % (
            res[1]['access_token'],
            res[1]['refresh_token'],
            res[1]['expires_in']
        ))

    if action == 'authorize':
        if len(sys.argv) == 2:
            print("Visit this URL to get a PIN to authorize: " + factory.get_api_url() + "oauth2/authorize?client_id=" + config['client_id'] + "&response_type=pin")
        if len(sys.argv) == 3:
            pin = sys.argv[2]
            imgur = factory.build_api()
            req = factory.build_request_oauth_token_swap('pin', pin)
            try:
                res = imgur.retrieve_raw(req)
            except HTTPError as e:
                print("Error %d\n%s" % (e.code, e.read().decode('utf8')))
                raise e
                
            print("Access Token: %s\nRefresh Token: %s\nExpires: %d seconds from now." % (
                res[1]['access_token'],
                res[1]['refresh_token'],
                res[1]['expires_in']
            ))


def handle_unauthorized_commands(factory, action):
    imgur = factory.build_api()
    req = None

    if action == 'upload':
        req = factory.build_request_upload_from_path(sys.argv[2])
        res = imgur.retrieve(req)

        print(res['link'])

    else:
        if action == 'list-comments':
            thash = sys.argv[2]
            req = factory.build_request(('gallery', thash, 'comments'))

        if action == 'get-album':
            id = sys.argv[2]
            req = factory.build_request(('album', id))

        if action == 'get-comment':
            (thash, cid) = sys.argv[2:4]
            req = factory.build_request(('gallery', thash, 'comments', cid))

        if action == 'get-gallery':
            imgur = factory.build_api()
            id = sys.argv[2]
            req = factory.build_request(('gallery', id))

        res = imgur.retrieve(req)
        print(res)


if __name__ == "__main__":
    main()
