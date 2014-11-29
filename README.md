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

The best way to reach out to Imgur for API support would be our
[Google Group](https://groups.google.com/forum/#!forum/imgur), [Twitter](https://twitter.com/imgurapi), or via
 api@imgur.com.

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

## Anonymous Usage without user authorization

### Print links in a Gallery
Output links from gallery could be a GalleyImage or GalleryAlbum

#### Default
By default, this will return links to items on the first page (0) with section 'hot' sorted by 'viral', date range is 'day' and show_viral is set to True

```python
items = client.gallery()
for item in items:
    print(item.link)

```

**Output**


    http://i.imgur.com/dRMIpvS.png
	http://imgur.com/a/uxKYS
	http://i.imgur.com/jYvaxQ1.jpg
	http://i.imgur.com/ZWQJSXp.jpg
	http://i.imgur.com/arP5ZwL.jpg
	http://i.imgur.com/BejpKnz.jpg
	http://i.imgur.com/4FJF0Vt.jpg
	http://i.imgur.com/MZSBjTP.jpg
	http://i.imgur.com/EbeztS2.jpg
	http://i.imgur.com/DuwnhKO.jpg
	...

#### With Specific Parameters
In this example, return links to items on the fourth page (3) with section 'top' sorted by 'time', date range is 'week' and show_viral is set to False

```python
items = client.gallery(section='top', sort='time', page=3, window='week', show_viral=False)
for item in items:
    print(item.link)

```

**Output**


    http://i.imgur.com/ls7OPx7.gif
	http://i.imgur.com/FI7yPWo.png
	http://imgur.com/a/8QKvH
	http://i.imgur.com/h4IDMyK.gif
	http://i.imgur.com/t4NpfCT.jpg
	http://i.imgur.com/kyCP6q9.jpg
	http://imgur.com/a/CU11w
	http://i.imgur.com/q4rJFbR.jpg
	http://i.imgur.com/gWaNC22.jpg
	http://i.imgur.com/YEQomCd.gif
	...

### Upload Image

#### Upload from URL
In this example, upload an image which is a URL

```python
image = client.upload_from_url('https://scontent-a-lga.xx.fbcdn.net/hphotos-xfp1/v/t1.0-9/10405254_855764424482474_6812608353091007109_n.jpg?oh=26f230eca9e55dde4021e0d11e3ccef0&oe=54D92A21')
print image

```
**Output**

    {u'account_url': None, u'deletehash': u'Nxrdpf7c6HZq5Zh', u'description': None, u'name': u'', u'title': None, u'section': None, u'views': 0, u'favorite': False, u'datetime': 1416694646, u'height': 852, u'width': 600, u'bandwidth': 0, u'nsfw': None, u'vote': None, u'link': u'http://i.imgur.com/iU03DTq.jpg', u'animated': False, u'type': u'image/jpeg', u'id': u'iU03DTq', u'size': 79631}
    

#### Upload from Path
In this example, upload an image which is a file

```python
image = client.upload_from_path('/tmp/aW0nDYd_460s.jpg')
print image

```

**Output**

    {u'account_url': None, u'deletehash': u'JuWydSGOZesuZSv', u'description': None, u'name': u'', u'title': None, u'section': None, u'views': 0, u'favorite': False, u'datetime': 1416695070, u'height': 451, u'width': 460, u'bandwidth': 0, u'nsfw': None, u'vote': None, u'link': u'http://i.imgur.com/Mcp6byc.jpg', u'animated': False, u'type': u'image/jpeg', u'id': u'Mcp6byc', u'size': 47306}

### Album

If you want to deal with anonymous albums, the following authentication is sufficient:

    client = ImgurClient(client_id, client_secret)

Else:

    client = ImgurClient(client_id, client_secret, access_token, refresh_token)

Following examples will assume you have authenticated with an account.

#### Create Albbum
Create a new album. To add images to an album during creation, you need to be authenticated with an account. Creating an album without authenticating an account will create an anonymous album which is not tied to an account. Adding images to an anonymous album is only available during image uploading. 

```python
fields = {'title' : 'Barcelona', 'description' : 'Test album for Imgur API Examples', 'layout' : 'vertical'}

print client.create_album(fields)
```

**Output**

    {u'deletehash': u'IctCbuL0f9VcmBh', u'id': u'9SsDk'}

#### Add Images to Album

```python
image1 =  client.upload_from_url('http://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/450px-FC_Barcelona_%28crest%29.svg.png', anon=False)
image1_id = image1['id']

image2 =  client.upload_from_url('http://arxiu.fcbarcelona.cat/web/downloads/sala_premsa/fotos/Plantilla0809/FCBarcelona0809.jpg')
image2_id = image2['id']

print client.album_add_images('9SsDk', [image1_id, image2_id])

```

**Output**

    True


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
* `create_album(fields)`
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
