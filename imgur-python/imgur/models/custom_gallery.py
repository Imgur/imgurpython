from gallery_album import GalleryAlbum
from gallery_image import GalleryImage


class CustomGallery:

    def __init__(self, id, name, datetime, account_url, link, tags, item_count=None, items=None):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.account_url = account_url
        self.link = link
        self.tags = tags
        self.item_count = item_count
        self.items = [GalleryAlbum(item) if item['is_album'] else GalleryImage(item) for item in items] \
            if items else None
