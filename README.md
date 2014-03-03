Imgur API Example Usage
=======================

This is a demo application of the [Imgur API](http://api.imgur.com/). It can be used to interrogate the Imgur API and
examine its responses, as a simple command line utility, and it can be used as a library for working with the Imgur API.

You must [register](http://api.imgur.com/oauth2/addclient) your client with the Imgur API, and provide the client ID to
do *any* request to the API. If you want to perform actions on accounts, the user will have to authorize it through OAuth.
The **secret** field is required for OAuth.

Usage
-----

> Usage:  python main.py (action) [options...]
> 
> ---------------------------------------------------------------------------------------------------------
> OAuth Actions
> ---------------------------------------------------------------------------------------------------------
> credits                          View the rate limit information for this client
> authorize                        Get the authorization URL
> authorize [pin]                  Get an access token
> 
> ---------------------------------------------------------------------------------------------------------
> Unauthorized Actions
> ---------------------------------------------------------------------------------------------------------
> upload [file]                    Anonymously upload a file
> album [id]                       View information about an album
> list-comment [hash]              Get the comments (raw json) for a gallery item
> comment-by-id [hash] [id]        Get a particular comment (raw json) for a gallery item
> gallery [hash]                   View information about a gallery post
> 
> ---------------------------------------------------------------------------------------------------------
> Authorized Actions
> ---------------------------------------------------------------------------------------------------------
> upload-auth [token] [file]       Upload a file to your account
> refresh [refresh-token]          Return a new OAuth access token after it's expired
> comment [token] [hash] [text]    Comment on a gallery image


Config
------

Configuration is done through the **config.json** file in JSON format. The contents of the file should be a JSON
object with the following properties:

### client_id

**Key**: 'client_id'

**Type**: String [16 characters]

**Description**: The client ID you got when you registered. Required for any API call. 

### secret

**Key**: 'secret'

**Type**: String [40 characters]

**Description**: The client secret you got when you registered, if you want to do OAuth authentication. 

### token_store

**Key**: 'token_store'

**Type**: Object

**Description**: Future configuration to control where the tokens are stored for persistent **insecure** storage of refresh tokens.
