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
> **upload-auth [access-token]**                
> Upload a file to your account
>
> **comment [access-token] [hash] [text ...]**  
> Comment on a gallery post
>
> **vote-gallery [token] [hash] [direction]**   
> Vote on a gallery post. Direction either 'up', 'down', or 'veto'
>
> **vote-comment [token] [id] [direction]**     
> Vote on a gallery comment. Direction either 'up', 'down', or 'veto'

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
