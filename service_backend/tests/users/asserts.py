"""Function asserts for tests"""
from urllib import parse
from backend.models import models


def correct_user(json):
    """Checks the json user contains the correct attributes."""
    assert 'sub' in json and type(json['sub']) is str
    assert 'iss' in json and type(json['iss']) is str
    assert 'email' in json and type(json['email']) is str
    assert 'created_at' in json and type(json['created_at']) is str

    return True


def match_user(json, user):
    """Checks the json elements matches the user object."""
    assert json['sub'] == user.sub
    assert json['iss'] == user.iss
    assert json['email'] == user.email
    assert json['created_at'] == str(user.created_at).replace(" ", "T")

    return True


def match_user_in_db(json):
    user_key = (json['sub'], json['iss'])
    db_user = models.User.query.get(user_key)
    assert match_user(json, db_user)

    return True


def match_query(json, url):
    """Checks the json elements matches the url query."""
    presult = parse.urlparse(url)
    for k, lv in parse.parse_qs(presult.query).items():
        assert lv[0] == json[k]

    return True


def match_search(json, url):
    """Checks the json elements matches the url search."""
    presult = parse.urlparse(url)
    dict_terms = dict(parse.parse_qs(presult.query).items())
    if dict_terms == {}:
        return True
    for term in dict_terms['terms']:
        assert json['email'].__contains__(term)

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
