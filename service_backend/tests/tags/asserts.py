"""Function asserts for tests"""
from urllib import parse


def match_tag(json, tag):
    """Checks the json tag contains the correct attributes."""

    # Check the tag has an id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(tag.id)

    # Check the tag has a name
    assert 'name' in json and type(json['name']) is str
    assert json['name'] == tag.name

    # Check the tag has a description
    assert 'description' in json and type(json['description']) is str
    assert json['description'] == tag.description

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
            json['description'].__contains__(term)
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
