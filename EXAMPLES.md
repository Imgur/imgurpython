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