import html
import requests
import re
from io import BytesIO
from PIL import Image
from dateutil import parser

from django.db.models import Q


CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def find_content_image(item):
    image_fields = ["media_content", "media_thumbnail", "links", "media_group", "enclosures", "image", "thumbnail"]
    for field in image_fields:
        if hasattr(item, field):
            value = getattr(item, field)
            if isinstance(value, list):
                for sub_field in value:
                    if isinstance(sub_field, dict) and "url" in sub_field:
                        url = sub_field["url"]
                    elif isinstance(value, dict) and "url" in value:
                        url = value["url"]
                    try:
                        response = requests.get(url, stream=True)
                        response.raise_for_status()
                        image = Image.open(BytesIO(response.content))
                        return url
                    except (requests.exceptions.HTTPError, IOError, Image.DecompressionBombWarning):
                        continue
    return None


def save_new_contents(feed, Content):
    """Saves new contents to the database.

    Checks the content GUID against the contents currently stored in the
    database. If not found, then a new `Content` is added to the database.

    Args:
        feed: requires a feedparser object
    """

    try:
        content_title = feed.channel.get('title', 'Technology')
    except AttributeError:
        content_title = "Technology"

    counter = 0
    for item in feed.entries:
        try:
            if counter >= 3:
                break
            guid = item.get('guid', item.get('id', ''))
            if not Content.objects.filter(Q(guid=guid) | Q(link=item.get('link', item.get('url', '')))).exists():
                content_image = find_content_image(item)
                tzinfos = {"PDT": -25200, "PST": -28800}  # PDT and PST offsets in seconds
                pub_date = parser.parse(item.get('published', item.get('updated', '')), tzinfos=tzinfos)
                description = html.unescape(cleanhtml(item.get('description', item.get('summary', ''))))
                content = Content(
                    title=item.get('title', item.get('name', '')),
                    description=description,
                    pub_date=pub_date,
                    link=item.get('link', item.get('url', '')),
                    content_name=content_title,
                    guid=guid,
                    image=content_image,
                )
                content.save()
                counter += 1
        except Exception as e:
            print(f"An error occurred while saving the contents for {content_title}: {e}")
