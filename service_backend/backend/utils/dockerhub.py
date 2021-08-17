import requests
from requests.exceptions import RequestException


registry_url = "https://registry.hub.docker.com/v2/repositories"


def valid_image(image, tag="latest"):
    try:
        image_req = requests.get(f"{registry_url}/{image}")
        image_meta = image_req.json()
        # If repository is private, return false
        if 'is_private' not in image_meta or image_meta['is_private']:
            return False

        tags_req = requests.get(f"{registry_url}/{image}/tags")
        tags_meta = tags_req.json()
        # search result with correct tag name
        return tag in (result['name'] for result in tags_meta['results'])

    except RequestException:
        return False
