from typing import Tuple


def decompose_dockername(docker_name: str) -> Tuple[str, str, str]:
    """Helper to break a model-docker_name into a tuple.

    Args:
        docker_name (str): Docker name to decompose.
    Returns:
        Tuple[str, str, str]: A tuple containing the username, the image name and the tag.
    """
    slash = docker_name.find('/')
    if slash == -1:
        # this should not have passed input validation
        pass
    username = docker_name[:slash]
    colon = docker_name.find(':')
    if colon == -1:
        image = docker_name[slash + 1:]
        tag = None
    else:
        image = docker_name[slash + 1:colon]
        tag = docker_name[colon + 1:]

    return username, image, tag


def build_dockerhub_url(docker_name: str) -> str:
    """Helper function to build a link to a docker hub page.

    Args:
        docker_name (str): The docker name to build a dockerhub url for.
    Returns:
        str: An URL to the given docker container on dockerhub.
    """
    (username, image, tag) = decompose_dockername(docker_name)

    url = 'https://hub.docker.com/r/{}/{}'.format(username, image)
    return url


def build_dockerregistry_url(docker_name: str) -> str:
    """Helper function to build a link to the docker hub registry api.

    Args:
        docker_name (str): The docker name to build a link to the docker registry for.
    Returns:
        str: An URL to the given docker container on the docker registry.
    """
    (username, image, tag) = decompose_dockername(docker_name)

    url = 'https://registry.hub.docker.com/v2/repositories/{}/{}/'.format(username, image)
    return url


def build_dockerregistry_tag_url(docker_name: str) -> str:
    """Helper function to build a link to the docker hub registry api.

    Returns:
        str: URL for the list of tags associated with the given image name from the docker hub registry.
    """
    (username, image, tag) = decompose_dockername(docker_name)

    url = 'https://registry.hub.docker.com/v2/repositories/{}/{}/tags'.format(username, image)
    return url
