imgurpython
===========

A Python client for the [Imgur API](http://api.imgur.com/). Also includes a friendly demo application. It can be used to
interact with the Imgur API and examine its responses, as a command line utility, and it can be used as a library
within your projects.

You must [register](http://api.imgur.com/oauth2/addclient) your client with the Imgur API, and provide the Client-ID to
make *any* request to the API (see the [Authentication](https://api.imgur.com/#authentication) note). If you want to
perform actions on accounts, the user will have to authorize your application through OAuth2.

Imgur API Documentation
-----------------------

Our developer documentation can be found [here](https://api.imgur.com/).

Community
---------

The best way to reach out to Imgur for API support would be our
[Google Group](https://groups.google.com/forum/#!forum/imgur), [Twitter](https://twitter.com/imgurapi), or via
 api@imgur.com.

Installation
------------

    pip install imgurpython

Configuration
-------------
`
Configuration is done through the **config.json** (placed in `imgur-python/data`) file in JSON format. The contents of the file should be a JSON
object with the following properties:

### client_id

**Key**: 'client_id'

**Type**: string [16 characters]

**Description**: The Client-ID you got when you registered. Required for any API call.

### secret

**Key**: 'secret'

**Type**: string [40 characters]

**Description**: The client secret you got when you registered, needed fo OAuth2 authentication.

### token_store

**Key**: 'token_store'

**Type**: object

**Description**: Future configuration to control where the tokens are stored for persistent **insecure** storage of refresh tokens.

Command Line Usage
------------------

> Usage:  python main.py (action) [options...]
>
> ### OAuth Actions
> 
> **credits**                                   
> View the rate limit information for this client
>
> **authorize**                                 
> Start the authorization process
>
> **authorize [pin]**                           
> Get an access token after starting authorization
>
> **refresh [refresh-token]**                   
> Return a new OAuth access token after it's expired
>
> ### Unauthorized Actions
> 
> **upload [file]**                             
> Anonymously upload a file
>
> **list-comments [hash]**                      
> Get the comments (raw JSON) for a gallery post
>
> **get-album [id]**                            
> Get information (raw JSON) about an album
>
> **get-comment [id]**                          
> Get a particular comment (raw JSON) for a gallery comment
>
> **get-gallery [hash]**                        
> Get information (raw JSON) about a gallery post
> 
> ### Authorized Actions
> 
> **upload-auth [access-token] [file]**
> Upload a file to your account
>
> **comment [access-token] [hash] [text]**
> Comment on a gallery post
>
> **vote-gallery [token] [hash] [direction]**   
> Vote on a gallery post. Direction can be either 'up', 'down', or 'veto'
>
> **vote-comment [token] [id] [direction]**     
> Vote on a gallery comment. Direction can be either 'up', 'down', or 'veto'