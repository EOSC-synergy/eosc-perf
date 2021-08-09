"""Function asserts for tests"""
from urllib import parse

from tests.asserts import match_benchmark, match_report, match_flavor, match_site, match_tag, match_user





def match_query(json, url):
    """Checks the json db_instances matches the url query."""
    presult = parse.urlparse(url)
    items = parse.parse_qs(presult.query)

    # Check the benchmark matches the request
    if 'docker_image' in items:
        assert json['benchmark']['docker_image'] == items['docker_image'][0]

    if 'docker_tag' in items:
        assert json['benchmark']['docker_tag'] == items['docker_tag'][0]

    # Check the site matches the request
    if 'site_name' in items:
        assert json['site']['name'] == items['site_name'][0]

    # Check the flavor matches the request
    if 'flavor_name' in items:
        assert json['flavor']['name'] == items['flavor_name'][0]

    # Check the tags matches the request
    tag_names = set(items.get('tag_names', []))
    assert tag_names.issubset(set(x['name'] for x in json['tags']))

    return True


def match_search(json, url):
    """Checks the json db_instances matches the url search."""
    presult = parse.urlparse(url)
    dict_terms = dict(parse.parse_qs(presult.query).items())
    if dict_terms == {}:
        return True
    for term in dict_terms['terms']:
        assert any([
            json['benchmark']['docker_image'].__contains__(term),
            json['benchmark']['docker_tag'].__contains__(term),
            json['site']['name'].__contains__(term),
            json['flavor']['name'].__contains__(term),
            any(tag['name'] == term for tag in json['tags'])
        ])

    return True


def match_body(json, body):
    """Checks the json db_instances matches the body dict."""
    if type(body) is list:
        for n in range(len(body)):
            match_body(json[n], body[n])
    elif type(body) is dict:
        for k in body:
            assert k in json
            match_body(json[k], body[k])
    else:
        assert json == body

    return True


def match_edit(json, body):
    # Check the benchmark matches the request
    if 'benchmark_id' in body:
        assert json['benchmark']['id'] == str(body['benchmark_id'])

    # Check the site matches the request
    if 'site_id' in body:
        assert json['site']['id'] == str(body['site_id'])

    # Check the flavor matches the request
    if 'flavor_id' in body:
        assert json['flavor']['id'] == str(body['flavor_id'])

    # Check the tags matches the request
    if 'tags_ids' in body:
        json_tags = set(t['id'] for t in json['tags'])
        body_tags = set(str(id) for id in body['tags_ids'])
        assert json_tags == body_tags

    return True
