"""Function asserts for tests"""
from urllib import parse


def correct_benchmark(json):
    """Checks the json benchmark contains the correct attributes."""
    assert 'id' in json and type(json['id']) is str
    assert 'docker_image' in json and type(json['docker_image']) is str
    assert 'docker_tag' in json and type(json['docker_tag']) is str
    assert 'description' in json and type(json['description']) is str
    assert 'json_template' in json and type(json['json_template']) is dict

    return True


def match_benchmark(json, benchmark):
    """Checks the json elements matches the benchmark object."""
    assert json['id'] == str(benchmark.id)
    assert json['docker_image'] == benchmark.docker_image
    assert json['docker_tag'] == benchmark.docker_tag
    assert json['description'] == benchmark.description
    assert json['json_template'] == benchmark.json_template

    return True


def match_query(json, url):
    """Checks the json elements matches the url query."""
    presult = parse.urlparse(url)
    for k, lv in parse.parse_qs(presult.query).items():
        item = [json[k]] if type(json[k]) is not list else json[k]
        assert lv == item

    return True


def match_search(json, url):
    """Checks the json elements matches the url search."""
    presult = parse.urlparse(url)
    dict_terms = dict(parse.parse_qs(presult.query).items())
    if dict_terms == {}:
        return True
    for term in dict_terms['terms']:
        assert any([
            json['docker_image'].__contains__(term),
            json['docker_tag'].__contains__(term),
            json['description'].__contains__(term)
        ])

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
