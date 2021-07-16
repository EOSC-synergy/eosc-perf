"""Function asserts for tests"""
from urllib import parse

from backend.reports import models
from tests.benchmarks.asserts import correct_benchmark, match_benchmark
from tests.results.asserts import correct_result, match_result
from tests.sites.asserts import (correct_flavor, correct_site, match_flavor,
                                 match_site)


def correct_report(json):
    """Checks the json result contains the correct attributes."""
    assert 'id' in json and type(json['id']) is str
    assert 'creation_date' in json and type(json['creation_date']) is str
    assert 'verdict' in json
    assert type(json['verdict']) is bool or json['verdict'] == None
    assert 'message' in json and type(json['message']) is str
    assert 'resource_type' in json and type(json['resource_type']) is str
    assert 'resource_id' in json and type(json['resource_id']) is str

    return True


def match_report(json, report):
    """Checks the json elements matches the report object."""
    assert json['id'] == str(report.id)
    assert json['creation_date'] == str(report.creation_date.date())
    assert json['verdict'] == report.verdict
    assert json['message'] == report.message
    assert json['resource_type'] == report.resource_type
    assert json['resource_id'] == str(report.resource_id)

    return True


def match_query(json, url):
    """Checks the json elements matches the url query."""
    presult = parse.urlparse(url)
    query_items = parse.parse_qs(presult.query)

    # Report checks
    if 'verdict' in query_items:
        assert str(json['verdict']) in query_items['verdict']

    if 'type' in query_items:
        assert str(json['type']) in query_items['type']

    if 'upload_before' in query_items:
        assert json['creation_date'] < query_items['created_before'][0]

    if 'upload_after' in query_items:
        assert json['creation_date'] > query_items['created_after'][0]

    return True


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

    return True
