"""Function asserts for tests"""
from urllib import parse
from backend.models import models


def match_user(json, user):
    """Checks the json db_instances matches the user object."""
    
    # Check the user has subject
    assert 'sub' in json and type(json['sub']) is str
    assert json['sub'] == user.sub

    # Check the user has issuer
    assert 'iss' in json and type(json['iss']) is str    
    assert json['iss'] == user.iss

    # Check the user has email
    assert 'email' in json and type(json['email']) is str
    assert json['email'] == user.email

    # Check the user has creation date
    assert 'created_at' in json and type(json['created_at']) is str
    assert json['created_at'] == str(user.created_at).replace(" ", "T")

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
        assert json['email'].__contains__(term)

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
