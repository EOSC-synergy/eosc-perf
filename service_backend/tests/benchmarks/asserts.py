"""Function asserts for tests"""
from urllib import parse


def correct_benchmark(json):
    """Checks the json benchmark contains the correct attributes."""
    assert 'id' in json and type(json['id']) is str
    assert 'docker_image' in json and type(json['docker_image']) is str
    assert 'docker_tag' in json and type(json['docker_tag']) is str


def match_benchmark(json, benchmark):
    """Checks the json elements matches the benchmark object."""
    assert json['id'] == str(benchmark.id)
    assert json['docker_image'] == benchmark.docker_image
    assert json['docker_tag'] == benchmark.docker_tag


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
