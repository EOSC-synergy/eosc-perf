import json
import urllib.request
from json import JSONDecodeError
from urllib.error import URLError


registry_url = "https://registry.hub.docker.com/v2/repositories"


def valid_image(image, tag="latest"):
    try:
        image_req = urllib.request.urlopen(f"{registry_url}/{image}")
        image_meta = json.loads(image_req.read())
        # If repository is private, return false
        if image_meta['is_private']:
            return False

        tags_req = urllib.request.urlopen(f"{registry_url}/{image}/tags")
        tags_meta = json.loads(tags_req.read())
        # search result with correct tag name
        return tag in (result['name'] for result in tags_meta['results'])

    except (URLError, JSONDecodeError):
        return False
