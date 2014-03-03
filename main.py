#!/usr/bin/env python3
import json, sys, time as dt, pprint

from Imgur.Factory import Factory
from Imgur.Auth.Expired import Expired

try:
    from urllib.request import urlopen as UrlLibOpen
    from urllib.request import HTTPError
except ImportError:
    from urllib2 import urlopen as UrlLibOpen
    from urllib2 import HTTPError


def main():
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

    if len(sys.argv) <= 1:
        sep = '---------------------------------------------------------------------------------------------------------'
        minisep = '-----------------------------------------------------'

        print("Usage: \tpython main.py (action) [options...]")
        print("\n" + sep + "\nOAuth Actions\n" + sep)
        print("credits                          View the rate limit information for this client")
        print("authorize                        Get the authorization URL")
        print("authorize [pin]                  Get an access token")
        print("refresh [refresh-token]          Return a new OAuth access token after it's expired")
        print("\n" + sep + "\nUnauthorized Actions\n" + sep)
        print("upload [file]                    Anonymously upload a file")
        print("album [id]                       View information about an album")
        print("list-comment [hash]              Get the comments (raw json) for a gallery item")
        print("comment-by-id [hash] [id]        Get a particular comment (raw json) for a gallery item")
        print("gallery [hash]                   View information about a gallery post")
        print("\n" + sep + "\nAuthorized Actions\n" + sep)
        print("upload-auth [token] [file]       Upload a file to your account")
        print("comment [token] [hash] [text]    Comment on a gallery image")
        sys.exit(1)

    action = sys.argv[1]

    authorized_actions = [
        'upload-auth',
        'refresh',
        'comment'
    ]

    if action in authorized_actions:
        handle_authorized_commands(factory, action)
    else:
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

        else:
            handle_unauthorized_commands(factory, action)

def handle_authorized_commands(factory, action):
    if action == 'refresh':
        token = sys.argv[2]
        imgur = factory.build_api()
        req = factory.build_request_oauth_refresh(token)

        try:
            res = imgur.retrieve_raw(req)
        except urllib.request.HTTPError as e:
            print("Error %d\n%s" % (e.code, e.read().decode('utf8')))
            raise e

        print('Access Token: %s\nRefresh Token: %s\nExpires: %d seconds from now.' % (
            res[1]['access_token'],
            res[1]['refresh_token'],
            res[1]['expires_in']
        ))

    if action == 'upload-auth':
        (token, path) = sys.argv[2:]
        auth = factory.build_oauth(token, None)
        imgur = factory.build_api(auth)
        req = factory.build_request_upload_from_path(path)
        try:
            res = imgur.retrieve(req)
            print(res['link'])
        except Expired:
            print("Expired access token")

    if action == 'comment':
        (token, thash) = sys.argv[2:4]
        text = ' '.join(sys.argv[4:])

        if len(text) > 140:
            print("Comment too long (trim by %d characters)." % (len(text) - 140))
            sys.exit(1)

        auth = factory.build_oauth(token, None)
        imgur = factory.build_api(auth)
        req = factory.build_request(('gallery', thash, 'comment'), {
            'comment': text
        })
        res = imgur.retrieve(req)
        print("Success! https://www.imgur.com/gallery/%s/comment/%s" % (thash, res['id']))

    if action == 'gallery':
        imgur = factory.build_api()
        req = factory.build_request(('gallery', id))
        res = imgur.retrieve(req)
        print(res)


def handle_unauthorized_commands(factory, action):
    imgur = factory.build_api()

    if action == 'upload':
        req = factory.build_request_upload_from_path(sys.argv[2])
        res = imgur.retrieve(req)
        print(res['link'])

    if action == 'credits':
        req = factory.build_request(('credits',))
        res = imgur.retrieve(req)
        print(res)

    if action == 'list-comment':
        thash = sys.argv[2]
        
        req = factory.build_request(('gallery', thash, 'comments'))
        res = imgur.retrieve(req)
        print(res)

    if action == 'album':
        id = sys.argv[2]
        
        req = factory.build_request(('album', id))
        res = imgur.retrieve(req)
        print(res)

    if action == 'vote':
        (token, thash, vote) = sys.argv[2:]
        auth = factory.build_oauth(token, None)
        imgur = factory.build_api(auth)
        req = factory.build_request(('gallery', thash, 'vote', vote), {"vote": vote})
        res = imgur.retrieve(req)
        print(res)

    if action == 'comment-by-id':
        (thash, cid) = sys.argv[2:4]
        
        req = factory.build_request(('gallery', thash, 'comments', cid))
        res = imgur.retrieve(req)
        print(res)


if __name__ == "__main__":
    main()
