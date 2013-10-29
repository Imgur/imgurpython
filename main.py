#!/usr/bin/env python3
import json, sys
from Imgur.Factory import Factory

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
        print("Usage: python3 main.py (action) [options...]")
        print("\nActions:\n")
        print("upload [file]                    Anonymously upload a file")
        print("authorize                        Get an access token")
        print("upload-auth [token] [file]       Upload a file to your account")
        print("comment [token] [hash] [text]    Comment on a gallery image")

    action = sys.argv[1]
    if action == 'upload':
        imgur = factory.buildAPI()
        req = factory.buildRequestUploadFromPath(sys.argv[2])
        res = imgur.retrieve(req)
        print(res['link'])

    if action == 'authorize':
        imgur = factory.buildAPI()
        req = factory.buildRequest()
        res = imgur.retrieve(req)
        
    if action == 'upload-auth':
        auth = factory.buildAuth()
        imgur = factory.buildAPI(auth)
        req = factory.buildRequestUploadFromPath(sys.argv[2])
        res = imgur.retrieve(req)
        print(res['link'])

    if action == 'comment':
        thash = sys.argv[2]
        text = ' '.join(sys.argv[3:])
        if len(text) > 140:
            print("Comment too long (trim by %d characters)." % (len(text) - 140))
            sys.exit(1)

        auth = factory.buildAuth()
        imgur = factory.buildAPI(auth)
        req = factory.buildRequestUploadFromPath(sys.argv[2])
        res = imgur.retrieve(req)

if __name__ == "__main__":
    main()
