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

#### Getting the authenticated user's albums

For endpoints that require usernames, once a user is authenticated we can use the keyword 'me' to pull their information. Here's how to pull one of their albums:
	
```python
for album in client.get_account_albums('me'):
album_title = album.title if album.title else 'Untitled'
print('Album: {0} ({1})'.format(album_title, album.id))

for image in client.get_album_images(album.id):
    image_title = image.title if image.title else 'Untitled'
    print('\t{0}: {1}'.format(image_title, image.link))

# Save some API credits by not getting all albums
break
```

***Output***


	Album: Qittens! (LPNnY)
		Untitled: http://i.imgur.com/b9rL7ew.jpg
		Untitled: http://i.imgur.com/Ymg3obW.jpg
		Untitled: http://i.imgur.com/kMzbu0S.jpg
		...


