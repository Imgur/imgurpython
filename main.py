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
    auth = factory.buildAuth('anonymous')
    imgur = factory.buildAPI(auth)
    req = factory.buildRequest(('gallery', 'hot'))
    res = imgur.retrieve(req)
    # print(res)
    

if __name__ == "__main__":
    main()
