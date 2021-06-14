"""Function asserts for tests"""
from urllib import parse


def correct_tag(json):
    """Checks the json tag contains the correct attributes."""
    assert 'id' in json and type(json['id']) is str
    assert 'name' in json and type(json['name']) is str
    assert 'description' in json and type(json['description']) is str


def match_tag(json, tag):
    """Checks the json elements matches the tag object."""
    assert json['id'] == str(tag.id)
    assert json['name'] == tag.name
    assert json['description'] == tag.description


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
