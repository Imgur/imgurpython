#!/usr/bin/env python3
import json, sys, time as dt, pprint, urllib
from Imgur.Factory import Factory
from Imgur.Auth.Expired import Expired

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
        print("Usage: python3 main.py (action) [options...]")
        print("\n" + sep + "\nUnauthorized Actions\n" + sep)
        print("upload [file]                    Anonymously upload a file")
        print("comments [hash]                  Get the comments (raw json) for a gallery item")
        print("comment-id [hash] [id]           Get a particular comment (raw json) for a gallery item")
        print("credits                          Inspect the rate limits for this client")
        print("authorize                        Get the authorization URL")
        print("authorize [pin]                  Get an access token")
        print("\n" + sep + "\nAuthorized Actions\n" + sep)
        print("upload-auth [token] [file]       Upload a file to your account")
        print("refresh [refresh-token]          Return a new OAuth access token after it's expired")
        print("comment [token] [hash] [text]    Comment on a gallery image")
        sys.exit(1)

    time = int(dt.time())
    action = sys.argv[1]

    if action == 'upload':
        imgur = factory.buildAPI()
        req = factory.buildRequestUploadFromPath(sys.argv[2])
        res = imgur.retrieve(req)
        print(res['link'])

    if action == 'credits':
        imgur = factory.buildAPI()
        req = factory.buildRequest(('credits',))
        res = imgur.retrieve(req)
        print(res)

    if action == 'authorize':
        if len(sys.argv) == 2:
            print("Visit this URL to get a PIN to authorize: " + factory.getAPIUrl() + "oauth2/authorize?client_id=" + config['client_id'] + "&response_type=pin")
        if len(sys.argv) == 3:
            pin = sys.argv[2]
            imgur = factory.buildAPI()
            req = factory.buildRequestOAuthTokenSwap('pin', pin)
            try:
                res = imgur.retrieveRaw(req)
            except urllib.request.HTTPError as e:
                print("Error %d\n%s" % (e.code, e.read().decode('utf8')))
                raise e
                
            print("Access Token: %s\nRefresh Token: %s\nExpires: %d seconds from now." % (
                res[1]['access_token'],
                res[1]['refresh_token'],
                res[1]['expires_in']
            ))

    if action == 'refresh':
        token = sys.argv[2]
        imgur = factory.buildAPI()
        req = factory.buildRequestOAuthRefresh(token)
        res = imgur.retrieveRaw(req)
        print('Access Token: %s\nRefresh Token: %s\nExpires: %d seconds from now.' % (
            res[1]['access_token'],
            res[1]['refresh_token'],
            res[1]['expires_in']
        ))
        
    if action == 'upload-auth':
        (token, path) = sys.argv[2:]
        auth = factory.buildOAuth(token, None, time+3600)
        imgur = factory.buildAPI(auth)
        req = factory.buildRequestUploadFromPath(path)
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

        auth = factory.buildOAuth(token, None, time+3600)
        imgur = factory.buildAPI(auth)
        req = factory.buildRequest(('gallery', thash, 'comment'), {
            'comment': text
        })
        res = imgur.retrieve(req)
        print("Success! https://www.imgur.com/gallery/%s/comment/%s" % (thash, res['id']))

    if action == 'comments':
        thash = sys.argv[2]
        
        imgur = factory.buildAPI()
        req = factory.buildRequest(('gallery', thash, 'comments'))
        res = imgur.retrieve(req)
        print(res)

    if action == 'comment-id':
        (thash, cid) = sys.argv[2:4]
        
        imgur = factory.buildAPI()
        req = factory.buildRequest(('gallery', thash, 'comments', cid))
        res = imgur.retrieve(req)
        print(res)

if __name__ == "__main__":
    main()
