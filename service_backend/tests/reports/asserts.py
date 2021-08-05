"""Function asserts for tests"""
from urllib import parse


def match_report(json, report):
    """Checks the json db_instances matches the report object."""

    # Check the report has an id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(report.id)

    # Check the report has a creation date
    assert 'created_at' in json and type(json['created_at']) is str
    assert json['created_at'] == str(report.created_at).replace(" ", "T")

    # Check the report has a verdict
    assert type(json['verdict']) is bool or json['verdict'] is None
    assert json['verdict'] == report.verdict

    # Check the report has a message
    assert 'message' in json and type(json['message']) is str
    assert json['message'] == report.message

    # Check the report has a resource_type
    assert 'resource_type' in json and type(json['resource_type']) is str
    assert json['resource_type'] == report.resource_type

    # Check the report has a resource_id
    assert 'resource_id' in json and type(json['resource_id']) is str
    assert json['resource_id'] == str(report.resource_id)

    return True


def match_query(json, url):
    """Checks the json db_instances matches the url query."""
    presult = parse.urlparse(url)
    query_items = parse.parse_qs(presult.query)

    # Report checks
    if 'verdict' in query_items:
        assert str(json['verdict']) in query_items['verdict']

    if 'type' in query_items:
        assert str(json['type']) in query_items['type']

    if 'upload_before' in query_items:
        assert json['created_at'] < query_items['created_before'][0]

    if 'upload_after' in query_items:
        assert json['created_at'] > query_items['created_after'][0]

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
