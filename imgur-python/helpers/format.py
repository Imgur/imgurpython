import math
from imgur.models.comment import Comment
from imgur.models.gallery_album import GalleryAlbum
from imgur.models.gallery_image import GalleryImage
from imgur.models.notification import Notification


def center_pad(s, length):
    num_dashes = float(length - len(s) - 2) / 2
    num_dashes_left = int(math.floor(num_dashes))
    num_dashes_right = int(math.ceil(num_dashes))

    return ('=' * num_dashes_left) + ' ' + s + ' ' + ('=' * num_dashes_right)


def two_column_with_period(left, right, length):
    num_periods = int(length - (len(left) + len(right) + 2))
    return left + ' ' + ('.' * num_periods) + ' ' + right


def build_comment_tree(children):
    children_objects = []
    for child in children:
        to_insert = Comment(child)
        to_insert.children = build_comment_tree(to_insert.children)
        children_objects.append(to_insert)

    return children_objects


def format_comment_tree(response):
    if isinstance(response, list):
        result = []
        for comment in response:
            formatted = Comment(comment)
            formatted.children = build_comment_tree(comment['children'])
            result.append(formatted)
    else:
        result = Comment(response)
        result.children = build_comment_tree(response['children'])

    return result


def build_gallery_images_and_albums(response):
        if isinstance(response, list):
            result = []
            for item in response:
                if item['is_album']:
                    result.append(GalleryAlbum(item))
                else:
                    result.append(GalleryImage(item))
        else:
            if response['is_album']:
                result = GalleryAlbum(response)
            else:
                result = GalleryImage(response)

        return result


def build_notifications(response):
    result = {
        'replies': [],
        'messages': [Notification(
            item['id'],
            item['account_id'],
            item['viewed'],
            item['content']
        ) for item in response['messages']]
    }

    for item in response['replies']:
        notification = Notification(
            item['id'],
            item['account_id'],
            item['viewed'],
            item['content']
        )
        notification.content = format_comment_tree(item['content'])
        result['replies'].append(notification)

    return result


def build_notification(item):
    notification = Notification(
            item['id'],
            item['account_id'],
            item['viewed'],
            item['content']
        )

    if 'comment' in notification.content:
        notification.content = format_comment_tree(item['content'])

    return notification
