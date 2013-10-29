#!/usr/bin/env python3
import json, sys
import Imgur.Factory

def main():
    config = None
    try:
        fd = open('config.json', 'r')
    except:
        print("config file [config.json] not found.")
        sys.exit(1)

    try:
        config = fd.read()
    except:
        print("invalid json in config file.")
        sys.exit(1)

    factory = Imgur.Factory(config)
    auth = factory.createAuthorization('authorization')
    imgur = factory.createAPI(auth)
    

if __name__ == "__main__":
    main()
