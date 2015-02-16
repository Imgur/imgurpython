#!/usr/bin/env python3

'''
	Here's how you go about authenticating yourself! The important thing to
	note here is that this script will be used in the other examples so
	set up a test user with API credentials and set them up in here.
'''

from imgurpython import ImgurClient

def get_input(string):
	''' Get input from console regardless of python 2 or 3 '''
	try:
		return raw_input(string)
	except:
		return input(string)

def get_config():
	''' More version compatibility stuff '''
	try:
		import ConfigParser
		return ConfigParser.ConfigParser()
	except:
		import configparser
		return configparser.ConfigParser()

def authenticate():
	# Get client ID and secret from auth.ini
	config = get_config()
	config.read('auth.ini')
	client_id = config['credentials']['client_id']
	client_secret = config['credentials']['client_secret']

	client = ImgurClient(client_id, client_secret)

	# Authorization flow, pin example (see docs for other auth types)
	authorization_url = client.get_auth_url('pin')

	print("Go to the following URL: {0}".format(authorization_url))

	# Read in the pin, handle Python 2 or 3 here.
	pin = get_input("Enter pin code: ")

	# ... redirect user to `authorization_url`, obtain pin (or code or token) ...
	credentials = client.authorize(pin, 'pin')
	client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

	print("Authentication successful! Here are the details:")
	print("   Access token:  {0}".format(credentials['access_token']))
	print("   Refresh token: {0}".format(credentials['refresh_token']))

	return client

# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
	authenticate()