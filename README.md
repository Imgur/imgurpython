# The imgurpython project is no longer supported.

imgurpython
===========

A Python client for the [Imgur API](http://api.imgur.com/). It can be used to
interact with the Imgur API in your projects.

You must [register](http://api.imgur.com/oauth2/addclient) your client with the Imgur API, and provide the Client-ID to
make *any* request to the API (see the [Authentication](https://api.imgur.com/#authentication) note). If you want to
perform actions on accounts, the user will have to authorize your application through OAuth2.

Requirements
------------

- Python >= 2.7
- [requests](http://docs.python-requests.org/en/latest/user/install/)

Imgur API Documentation
-----------------------

Our developer documentation can be found [here](https://api.imgur.com/).

Community
---------

The best way to reach out to Imgur for API support is emailing us at api@imgur.com.

Installation
------------

    pip install imgurpython

Library Usage
------------

Using imgurpython in your application takes just a couple quick steps.

To use the client from a strictly anonymous context (no actions on behalf of a user)

```python

from imgurpython import ImgurClient

client_id = 'YOUR CLIENT ID'
client_secret = 'YOUR CLIENT SECRET'

client = ImgurClient(client_id, client_secret)

# Example request
items = client.gallery()
for item in items:
    print(item.link)

```

To initialize a client that takes actions on behalf of a user

```python
from imgurpython import ImgurClient

client_id = 'YOUR CLIENT ID'
client_secret = 'YOUR CLIENT SECRET'

client = ImgurClient(client_id, client_secret)

# Authorization flow, pin example (see docs for other auth types)
authorization_url = client.get_auth_url('pin')

# ... redirect user to `authorization_url`, obtain pin (or code or token) ...

credentials = client.authorize('PIN OBTAINED FROM AUTHORIZATION', 'pin')
client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
```

or if you already have an access/refresh token pair you can simply do

```python
from imgurpython import ImgurClient

# If you already have an access/refresh pair in hand
client_id = 'YOUR CLIENT ID'
client_secret = 'YOUR CLIENT SECRET'
access_token = 'USER ACCESS TOKEN'
refresh_token = 'USER REFRESH TOKEN'

# Note since access tokens expire after an hour, only the refresh token is required (library handles autorefresh)
client = ImgurClient(client_id, client_secret, access_token, refresh_token)
```

### Error Handling
Error types
* ImgurClientError - General error handler, access message and status code via

```python
from imgurpython.helpers.error import ImgurClientError

try
    ...
except ImgurClientError as e
    print(e.error_message)
    print(e.status_code)
```

* ImgurClientRateLimitError - Rate limit error

### Credits

To view client and user credit information, use the `credits` attribute of `ImgurClient`.
`credits` holds a dictionary with the following keys:
* UserLimit
* UserRemaining
* UserReset
* ClientLimit
* ClientRemaining

For more information about rate-limiting, please see the note in our [docs](http://api.imgur.com/#limits)!

Examples
------------
Examples can be found [here](EXAMPLES.md)

## ImgurClient Functions

### Account

* `get_account(username)`
* `get_gallery_favorites(username)`
* `get_account_favorites(username)`
* `get_account_submissions(username, page=0)`
* `get_account_settings(username)`
* `change_account_settings(username, fields)`
* `get_email_verification_status(username)`
* `send_verification_email(username)`
* `get_account_albums(username, page=0)`
* `get_account_album_ids(username, page=0)`
* `get_account_album_count(username)`
* `get_account_comments(username, sort='newest', page=0)`
* `get_account_comment_ids(username, sort='newest', page=0)`
* `get_account_comment_count(username)`
* `get_account_images(username, page=0)`
* `get_account_image_ids(username, page=0)`
* `get_account_album_count(username)`

### Album
* `get_album(album_id)`
* `get_album_images(album_id)`
* `create_album(fields)`
* `update_album(album_id, fields)`
* `album_delete(album_id)`
* `album_favorite(album_id)`
* `album_set_images(album_id, ids)`
* `album_add_images(album_id, ids)`
* `album_remove_images(album_id, ids)`

### Comment
* `get_comment(comment_id)`
* `delete_comment(comment_id)`
* `get_comment_replies(comment_id)`
* `post_comment_reply(comment_id, image_id, comment)`
* `comment_vote(comment_id, vote='up')`
* `comment_report(comment_id)`

### Custom Gallery

* `get_custom_gallery(gallery_id, sort='viral', window='week', page=0)`
* `get_user_galleries()`
* `create_custom_gallery(name, tags=None)`
* `custom_gallery_update(gallery_id, name)`
* `custom_gallery_add_tags(gallery_id, tags)`
* `custom_gallery_remove_tags(gallery_id, tags)`
* `custom_gallery_delete(gallery_id)`
* `filtered_out_tags()`
* `block_tag(tag)`
* `unblock_tag(tag)`

### Gallery

* `gallery(section='hot', sort='viral', page=0, window='day', show_viral=True)`
* `memes_subgallery(sort='viral', page=0, window='week')`
* `memes_subgallery_image(item_id)`
* `subreddit_gallery(subreddit, sort='time', window='week', page=0)`
* `subreddit_image(subreddit, image_id)`
* `gallery_tag(tag, sort='viral', page=0, window='week')`
* `gallery_tag_image(tag, item_id)`
* `gallery_item_tags(item_id)`
* `gallery_tag_vote(item_id, tag, vote)`
* `gallery_search(q, advanced=None, sort='time', window='all', page=0)`
* `gallery_random(page=0)`
* `share_on_imgur(item_id, title, terms=0)`
* `remove_from_gallery(item_id)`
* `gallery_item(item_id)`
* `report_gallery_item(item_id)`
* `gallery_item_vote(item_id, vote='up')`
* `gallery_item_comments(item_id, sort='best')`
* `gallery_comment(item_id, comment)`
* `gallery_comment_ids(item_id)`
* `gallery_comment_count(item_id)`

### Image

* `get_image(image_id)`
* `upload_from_path(path, config=None, anon=True)`
* `upload_from_url(url, config=None, anon=True)`
* `delete_image(image_id)`
* `favorite_image(image_id)`

### Conversation

* `conversation_list()`
* `get_conversation(conversation_id, page=1, offset=0)`
* `create_message(recipient, body)`
* `delete_conversation(conversation_id)`
* `report_sender(username)`
* `block_sender(username)`

### Notification

* `get_notifications(new=True)`
* `get_notification(notification_id)`
* `mark_notifications_as_read(notification_ids)`

### Memegen

* `default_memes()`

Imgur entry points
==================
| entry point                         |  content                       |
|-------------------------------------|--------------------------------|
| imgur.com/{image_id}                | image                          |
| imgur.com/{image_id}.extension      | direct link to image (no html) |
| imgur.com/a/{album_id}              | album                          |
| imgur.com/a/{album_id}#{image_id}   | single image from an album     |
| imgur.com/gallery/{gallery_post_id} | gallery                        |

