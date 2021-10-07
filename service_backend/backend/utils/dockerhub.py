"""Utils subpackage that contains all the constants, functions or
classes to interface the application with Docker Hub.
"""
import requests
from requests.exceptions import RequestException
from json import JSONDecodeError

#: Url where docker repositories can be queried
registry_url = "https://registry.hub.docker.com/v2/repositories"


def valid_image(image, tag="latest"):
    """Checks in docker hub the image:tag exists and that it is not
    private.

    :param image: Container identification to search in Docker Hub repository
    :type image: string
    :param tag: Container version to search for, defaults to "latest"
    :type tag: str, optional
    :return: True if image:tag exists and public, False otherwise
    :rtype: bool
    """
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

    except JSONDecodeError:
        return False
