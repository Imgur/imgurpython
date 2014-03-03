Imgur API Example Usage
=======================

This is a demo application of the [Imgur API](http://api.imgur.com/). It can be used to interrogate the Imgur API and
examine its responses, as a simple command line utility, and it can be used as a library for working with the Imgur API.

You must [register](http://api.imgur.com/oauth2/addclient) your client with the Imgur API, and provide the client ID to
do *any* request to the API. If you want to perform actions on accounts, the user will have to authorize it through OAuth.
The *secret* field is required for OAuth.

Config
------

Configuration is done through the *config.json* file in JSON format. The contents of the file should be a JSON
object with the following properties:

### client_id

**key**: 'client_id'
**type**: String [16 characters]
The client ID you got when you registered. Required for any API call. 

### secret

**key**: 'secret'
**type**: String [40 characters]
The client secret you got when you registered, if you want to do OAuth authentication. 

### token_store

**key**: 'token_store'
**type**: Object
Future configuration to control where the tokens are stored for persistent **insecure** storage of refresh tokens.
