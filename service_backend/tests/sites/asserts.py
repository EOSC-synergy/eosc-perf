"""Function asserts for tests"""
from urllib import parse

from backend.models import models


def match_site(json, site):
    """Checks the json db_instances matches the site object."""

    # Check the site has id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(site.id)

    # Check the site has name
    assert 'name' in json and type(json['name']) is str
    assert json['name'] == site.name

    # Check the site has address
    assert 'address' in json and type(json['address']) is str
    assert json['address'] == site.address

    # Check the site has description
    assert 'description' in json and type(json['description']) is str
    assert json['description'] == site.description

    return True


def match_flavor(json, flavor):
    """Checks the json db_instances matches the flavor object."""

    # Check the flavor has id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(flavor.id)

    # Check the flavor has name
    assert 'name' in json and type(json['name']) is str
    assert json['name'] == flavor.name

    # Check the flavor has description
    assert 'description' in json and type(json['description']) is str
    assert json['description'] == flavor.description

    return True


def match_query(json, url):
    """Checks the json db_instances matches the url query."""
    presult = parse.urlparse(url)
    for k, lv in parse.parse_qs(presult.query).items():
        assert lv[0] == json[k]

    return True


def match_search(json, url):
    """Checks the json db_instances matches the url search."""
    presult = parse.urlparse(url)
    dict_terms = dict(parse.parse_qs(presult.query).items())
    if dict_terms == {}:
        return True
    for term in dict_terms['terms']:
        assert any([
            json['name'].__contains__(term),
            json['address'].__contains__(term),
            json['description'].__contains__(term),
        ])

    return True


def match_body(json, body):
    """Checks the json db_instances matches the body dict."""
    for k in body:
        assert k in json
        if type(body[k]) is dict:
            assert type(json[k]) is dict
            match_body(json[k], body[k])
        if type(body[k]) is list:
            assert type(json[k]) is list
            for n in range(len(body[k])):
                match_body(json[k][n], body[k][n])
        else:
            assert body[k] == json[k]

    return True
