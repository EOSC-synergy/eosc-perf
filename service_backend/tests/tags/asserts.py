"""Function asserts for tests"""
from urllib import parse
from backend.tags import models


def correct_tag(json):
    """Checks the json tag contains the correct attributes."""
    assert 'id' in json and type(json['id']) is str
    assert 'name' in json and type(json['name']) is str
    assert 'description' in json and type(json['description']) is str

    return True


def match_tag(json, tag):
    """Checks the json elements matches the tag object."""
    assert json['id'] == str(tag.id)
    assert json['name'] == tag.name
    assert json['description'] == tag.description

    return True


def match_tag_in_db(json):
    db_tag = models.Tag.query.get(json['id'])
    assert match_tag(json, db_tag)

    return True


def match_query(json, url):
    """Checks the json elements matches the url query."""
    presult = parse.urlparse(url)
    for k, lv in parse.parse_qs(presult.query).items():
        assert lv[0] == json[k]

    return True


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

    return True
