"""Function asserts for tests"""
from urllib import parse

from backend.sites import models


def correct_site(json):
    """Checks the json site contains the correct attributes."""
    assert 'id' in json and type(json['id']) is str
    assert 'name' in json and type(json['name']) is str
    assert 'address' in json and type(json['address']) is str
    assert 'flavors' in json
    for flavor_json in json['flavors']:
        correct_flavor(flavor_json)


def match_site(json, site):
    """Checks the json elements matches the site object."""
    assert json['id'] == str(site.id)
    assert json['name'] == site.name
    assert json['address'] == site.address
    for n in range(len(site.flavors)):
        match_flavor(json['flavors'][n], site.flavors[n])


def correct_flavor(json):
    """Checks the json flavor contains the correct attributes."""
    assert 'name' in json and type(json['name']) is str
    assert 'description' in json and type(json['description']) is str


def match_flavor(json, flavor):
    """Checks the json elements matches the flavor object."""
    assert json['name'] == flavor.name
    assert json['description'] == flavor.description


def match_query(json, url):
    """Checks the json elements matches the url query."""
    presult = parse.urlparse(url)
    for k, lv in parse.parse_qs(presult.query).items():
        assert lv[0] == json[k]


def match_body(json, body):
    """Checks the json elements matches the body dict."""
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


def site_has_flavor(json, url):
    """Checks the json elements matches the site object."""
    presult = parse.urlparse(url)
    site_id = presult.path.split('/')[2]
    site = models.Site.get_by_id(site_id)
    flavors_names = [x.name for x in site.flavors]
    assert json['name'] in flavors_names
