"""Function asserts for tests"""
from urllib import parse

from backend.extensions import mail


def match_pagination(json, url):
    """Checks the json is a pagination object."""
    parsed_url = parse.urlparse(url)
    query_param = parse.parse_qs(parsed_url.query)

    assert 'has_next' in json and type(json['has_next']) is bool
    assert 'has_prev' in json and type(json['has_prev']) is bool
    assert 'total' in json and type(json['total']) is int
    assert 'items' in json and type(json['items']) is list
    assert 'pages' in json and type(json['pages']) is int
    assert 'per_page' in json and type(json['per_page']) is int
    assert 'page' in json and type(json['page']) is int

    # Pagination checks
    if 'per_page' in query_param:
        assert json['per_page'] == query_param['per_page'][0]
    if 'page' in query_param:
        assert json['page'] == query_param['page'][0]

    return True


def match_benchmark(json, benchmark):
    """Checks the json db_instances matches the benchmark object."""

    # Check the benchmark has an id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(benchmark.id)

    # Check the benchmark has a docker_image
    assert 'docker_image' in json and type(json['docker_image']) is str
    assert json['docker_image'] == benchmark.docker_image

    # Check the benchmark has a docker_tag
    assert 'docker_tag' in json and type(json['docker_tag']) is str
    assert json['docker_tag'] == benchmark.docker_tag

    # Check the benchmark has a description
    if 'description' in json:
        assert type(json['description']) is str
        assert json['description'] == benchmark.description

    # Check the benchmark has a json_schema
    assert 'json_schema' in json and type(json['json_schema']) is dict
    assert json['json_schema'] == benchmark.json_schema

    return True


def match_submit(json):
    """Checks the json db_instances matches the submit object."""

    # Check the report has an id
    assert 'id' not in json

    # Check the report has a upload date
    assert 'upload_datetime' in json
    assert type(json['upload_datetime']) is str

    # Check the report has a resource_type
    assert 'resource_type' in json and type(json['resource_type']) is str

    # Check the report has a resource_id
    assert 'resource_id' in json and type(json['resource_id']) is str

    # Check the submit has a uploader
    assert 'uploader' in json  # Submits should only be accessible by admins

    return True


def match_claim(json, claim):
    """Checks the json db_instances matches the claim object."""

    # Check the report has an id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(claim.id)

    # Check the report has a upload date
    assert 'upload_datetime' in json
    assert type(json['upload_datetime']) is str
    upload_datetime = str(claim.upload_datetime).replace(" ", "T")
    assert json['upload_datetime'] == upload_datetime

    # Check the report has a message
    assert 'message' in json and type(json['message']) is str
    assert json['message'] == claim.message

    # Check the report has a resource_type
    assert 'resource_type' in json and type(json['resource_type']) is str
    assert json['resource_type'] == claim.resource_type

    # Check the report has a resource_id
    assert 'resource_id' in json and type(json['resource_id']) is str
    assert json['resource_id'] == str(claim.resource_id)

    # Check the report has a uploader
    assert 'uploader' in json  # Reports should only be accessible by admins
    assert match_user(json['uploader'], claim.uploader)

    return True


def match_site(json, site):
    """Checks the json db_instances matches the site object."""

    # Check the site has id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(site.id)

    # Check the site has name
    assert 'name' in json and type(json['name']) is str
    assert json['name'] == site.name

    # Check the site has address
    assert 'address' in json and type(json['address']) is str
    assert json['address'] == site.address

    # Check the site has description
    if 'description' in json:
        assert type(json['description']) is str
        assert json['description'] == site.description

    return True


def match_flavor(json, flavor):
    """Checks the json db_instances matches the flavor object."""

    # Check the flavor has id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(flavor.id)

    # Check the flavor has name
    assert 'name' in json and type(json['name']) is str
    assert json['name'] == flavor.name

    # Check the flavor has description
    if 'description' in json:
        assert type(json['description']) is str
        assert json['description'] == flavor.description

    return True


def match_tag(json, tag):
    """Checks the json tag contains the correct attributes."""

    # Check the tag has an id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(tag.id)

    # Check the tag has a name
    assert 'name' in json and type(json['name']) is str
    assert json['name'] == tag.name

    # Check the tag has a description
    if 'description' in json:
        assert type(json['description']) is str
        assert json['description'] == tag.description

    return True


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

    return True


def match_result(json, result):
    """Checks the json db_instances matches the result object."""

    # Check the result has an id
    assert 'id' in json and type(json['id']) is str
    assert json['id'] == str(result.id)

    # Check the result has a json
    assert 'json' in json and type(json['json']) is dict
    assert json['json'] == result.json

    # Check the result has an upload date
    assert 'upload_datetime' in json
    assert type(json['upload_datetime']) is str
    upload_datetime = str(result.upload_datetime).replace(" ", "T")
    assert json['upload_datetime'] == upload_datetime

    # Check the report has a upload date
    assert 'execution_datetime' in json
    assert type(json['execution_datetime']) is str
    execution_datetime = str(result.execution_datetime).replace(" ", "T")
    assert json['execution_datetime'] == execution_datetime

    # Check the result has a benchmark
    assert 'benchmark' in json
    assert match_benchmark(json['benchmark'], result.benchmark)

    # Check the result has a site
    assert 'site' in json
    assert match_site(json['site'], result.site)

    # Check the result has a flavor
    assert 'flavor' in json
    assert match_flavor(json['flavor'], result.flavor)

    # Check the result has tags
    assert 'tags' in json and type(json['tags']) is list
    for json, tag in zip(json['tags'], result.tags):
        assert match_tag(json, tag)

    return True


def match_query(json, url):
    """Checks the json db_instances matches the url query."""
    parsed_url = parse.urlparse(url)
    query_param = parse.parse_qs(parsed_url.query)

    # Exclusive for /benchmarks
    if parsed_url.path == "/benchmarks":
        if 'docker_image' in query_param:
            assert json['docker_image'] == query_param['docker_image'][0]
        if 'docker_tag' in query_param:
            assert json['docker_tag'] == query_param['docker_tag'][0]

    # Exclusive for /benchmarks/search
    if parsed_url.path == "/benchmarks/search":
        for term in query_param.get('terms', []):
            assert any([
                json['docker_image'].__contains__(term),
                json['docker_tag'].__contains__(term),
                json['description'].__contains__(term)
            ])

    # Exclusive for /reports
    if parsed_url.path == "/reports/submits":
        if 'resource_type' in query_param:
            assert json['resource_type'] == query_param['resource_type'][0]
        if 'upload_before' in query_param:
            assert json['upload_datetime'] < query_param['upload_before'][0]
        if 'upload_after' in query_param:
            assert json['upload_datetime'] > query_param['upload_after'][0]

    # Exclusive for /reports
    if parsed_url.path == "/reports/claims":
        if 'upload_before' in query_param:
            assert json['upload_datetime'] < query_param['upload_before'][0]
        if 'upload_after' in query_param:
            assert json['upload_datetime'] > query_param['upload_after'][0]

    # Exclusive for /results
    if parsed_url.path == "/results":
        if 'docker_image' in query_param:
            assert json['benchmark']['docker_image']\
                == query_param['docker_image'][0]
        if 'docker_tag' in query_param:
            assert json['benchmark']['docker_tag']\
                == query_param['docker_tag'][0]
        if 'site_name' in query_param:
            assert json['site']['name']\
                == query_param['site_name'][0]
        if 'flavor_name' in query_param:
            assert json['flavor']['name']\
                == query_param['flavor_name'][0]
        if 'upload_before' in query_param:
            assert json['upload_datetime']\
                < query_param['upload_before'][0]
        if 'upload_after' in query_param:
            assert json['upload_datetime']\
                > query_param['upload_after'][0]
        if 'tag_names' in query_param:
            assert set(x['name'] for x in json['tags'])\
                == set(query_param['tag_names'])
        # Add assert for filters
            # TODO: Assert for filters

    # Exclusive for /results/search
    if parsed_url.path == "/results/search":
        for term in query_param.get('terms', []):
            assert any([
                json['benchmark']['docker_image'].__contains__(term),
                json['benchmark']['docker_tag'].__contains__(term),
                json['site']['name'].__contains__(term),
                json['flavor']['name'].__contains__(term),
                any(tag['name'] == term for tag in json['tags'])
            ])

    # Exclusive for /sites
    if parsed_url.path == "/sites":
        if 'name' in query_param:
            assert json['name'] == query_param['name'][0]
        if 'address' in query_param:
            assert json['address'] == query_param['address'][0]

    # Exclusive for /sites/search
    if parsed_url.path == "/sites/search":
        for term in query_param.get('terms', []):
            assert any([
                json['name'].__contains__(term),
                json['address'].__contains__(term),
                json['description'].__contains__(term),
            ])

    # Exclusive for /sites/{id}/flavors
    if parsed_url.path.__contains__("/sites") & \
       parsed_url.path.__contains__("/flavors"):
        if 'name' in query_param:
            assert json['name'] == query_param['name'][0]

    # Exclusive for /tags
    if parsed_url.path == "/tags":
        if 'name' in query_param:
            assert json['name'] == query_param['name'][0]

    # Exclusive for /tags/search
    if parsed_url.path == "/tags/search":
        for term in query_param.get('terms', []):
            assert any([
                json['name'].__contains__(term),
                json['description'].__contains__(term)
            ])

    # Exclusive for /users
    if parsed_url.path == "/users":
        if 'email' in query_param:
            assert json['email'] == query_param['email'][0]

    # Exclusive for /users/search
    if parsed_url.path == "/users/search":
        for term in query_param.get('terms', []):
            assert any([
                json['email'].__contains__(term),
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


def match_edit(json, body):
    """Checks the json edit response matches the request body."""

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


def submit_notification(report):
    """Checks a report notification is in the outbox"""
    mail_outbox = mail.get_connection().mailman.outbox

    def filter(item):
        headers = {'Resource-ID': str(report.resource.id)}
        chk1 = headers.items() <= item.extra_headers.items()
        chk2 = "submitted" in item.subject
        return chk1 and chk2

    envelope = pop_notification(mail_outbox, filter)
    assert envelope.from_email == "no-reply@example.com"
    assert report.resource.uploader.email in envelope.to
    assert "support@example.com" in envelope.cc


def user_welcome(user):
    """Checks a user welcome is in the outbox"""
    mail_outbox = mail.get_connection().mailman.outbox

    def filter(item):
        chk1 = "Thank you for registering" in item.subject
        return chk1

    envelope = pop_notification(mail_outbox, filter)
    assert envelope.from_email == "no-reply@example.com"
    assert user.email in envelope.to
    assert envelope.cc == []


def pop_notification(mail_outbox, filter):
    for index, item in enumerate(mail_outbox):
        if filter(item):
            return mail_outbox.pop(index)
    raise KeyError("Message not found")
