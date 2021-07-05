"""Function asserts for tests"""
from urllib import parse

from backend.results import models


def correct_result(json):
    """Checks the json result contains the correct attributes."""
    assert 'id' in json and type(json['id']) is str
    assert 'json' in json and type(json['json']) is dict
    assert 'benchmark_image' in json and type(json['benchmark_image']) is str
    assert 'benchmark_tag' in json and type(json['benchmark_tag']) is str
    assert 'site_name' in json and type(json['site_name']) is str
    assert 'flavor_name' in json and type(json['flavor_name']) is str
    assert 'tag_names' in json and type(json['tag_names']) is list
    for tag in json['tag_names']:
        assert type(tag) is str


def match_result(json, result):
    """Checks the json elements matches the result object."""
    assert json['id'] == str(result.id)
    assert json['json'] == result.json
    assert json['benchmark_image'] == result.benchmark.docker_image
    assert json['benchmark_tag'] == result.benchmark.docker_tag
    assert json['site_name'] == result.site.name
    assert json['flavor_name'] == result.flavor.name
    assert json['tag_names'] == result.tag_names


def match_query(json, url):
    """Checks the json elements matches the url query."""
    presult = parse.urlparse(url)
    for k, lv in parse.parse_qs(presult.query).items():
        item = [json[k]] if type(json[k]) is not list else json[k]
        assert lv == item


def match_body(json, body):
    """Checks the json elements matches the body dict."""
    if type(body) is list:
        for n in range(len(body)):
            match_body(json[n], body[n])
    elif type(body) is dict:
        for k in body:
            assert k in json
            match_body(json[k], body[k])
    else:
        assert json == body


def result_has_flavor(json, url):
    """Checks the json elements matches the result object."""
    presult = parse.urlparse(url)
    result_id = presult.path.split('/')[2]
    result = models.Result.get_by_id(result_id)
    flavors_names = [x.name for x in result.flavors]
    assert json['name'] in flavors_names
