"""Function asserts for tests"""
from urllib import parse


def correct_user(json):
    """Checks the json user contains the correct attributes."""
    assert 'sub' in json and type(json['sub']) is str
    assert 'iss' in json and type(json['iss']) is str
    assert 'email' in json and type(json['email']) is str
    assert 'created_at' in json and type(json['created_at']) is str


def match_user(json, user):
    """Checks the json elements matches the user object."""
    assert json['sub'] == user.sub
    assert json['iss'] == user.iss
    assert json['email'] == user.email
    assert json['created_at'] == str(user.created_at)


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
