"""Module with db elements specifications for factories"""
from uuid import uuid4
from datetime import datetime


# Tags specifications
tag_1 = {'id': uuid4(), 'name': "tag1"}
tag_1['description'] = "Description tag 1"

tag_2 = {'id': uuid4(), 'name': "tag2"}
tag_2['description'] = "Description tag 2"

tag_3 = {'id': uuid4(), 'name': "tag3"}
tag_3['description'] = "Description tag 3"

tag_4 = {'id': uuid4(), 'name': "tag4"}
tag_4['description'] = "Description tag 4"


# Benchmark specifications
benchmark_1 = {'id': uuid4(), 'docker_image': "b1", 'docker_tag': "v1.0"}
benchmark_1['description'] = "Benchmark 1"
benchmark_1['json_template'] = {'time': ""}

benchmark_2 = {'id': uuid4(), 'docker_image': "b1", 'docker_tag': "v2.0"}
benchmark_2['description'] = "Benchmark 1"
benchmark_2['json_template'] = {'time': ""}

benchmark_3 = {'id': uuid4(), 'docker_image': "b2", 'docker_tag': "v1.0"}
benchmark_3['description'] = "Benchmark 2"
benchmark_3['json_template'] = {'time': ""}


def sub_benchmark(benchmark, element):
    element['benchmark__id'] = benchmark['id']
    element['benchmark__docker_image'] = benchmark['docker_image']
    element['benchmark__docker_tag'] = benchmark['docker_tag']
    element['benchmark__description'] = benchmark['description']
    element['benchmark__json_template'] = benchmark['json_template']


# Site specifications
site_1 = {'id': uuid4(), 'name': "site1", 'address': "address1"}
site_1['description'] = "Text"

site_2 = {'id': uuid4(), 'name': "site2", 'address': "address2"}
site_2['description'] = "Text"


def sub_site(site, element):
    element['site__id'] = site['id']
    element['site__name'] = site['name']
    element['site__address'] = site['address']
    element['site__description'] = site['description']


# Flavor specifications
flavor_1 = {'id': uuid4(), 'name': "flavor1"}
flavor_1['description'] = "Flavor1 site1"
flavor_1['site_id'] = site_1['id']

flavor_2 = {'id': uuid4(), 'name': "flavor2"}
flavor_2['description'] = "Flavor2 site1"
flavor_2['site_id'] = site_1['id']

flavor_3 = {'id': uuid4(), 'name': "flavor1"}
flavor_3['description'] = "Flavor1 site2"
flavor_3['site_id'] = site_2['id']


def sub_flavor(flavor, element):
    element['flavor__id'] = flavor['id']
    element['flavor__name'] = flavor['name']
    element['flavor__description'] = flavor['description']


# User specifications
user_1 = {'sub': "sub_1",  'iss': "egi.com"}
user_1['email'] = "sub_1@email.com"

user_2 = {'sub': "sub_2",  'iss': "egi.com"}
user_2['email'] = "sub_2@email.com"


def sub_user(user, element):
    element['uploader__sub'] = user['sub']
    element['uploader__iss'] = user['iss']
    element['uploader__email'] = user['email']


# Result specifications
result_1 = {'id': uuid4(), 'json': {'time': 10}}
result_1['upload_date'] = datetime(2000, 1, 1)
result_1['tags'] = [tag_1, tag_2]
sub_benchmark(benchmark_1, result_1)
sub_site(site_1, result_1)
sub_flavor(flavor_1, result_1)
sub_user(user_1, result_1)

result_2 = {'id': uuid4(), 'json': {'time': 12}}
result_2['upload_date'] = datetime(2010, 1, 1)
result_2['tags'] = [tag_1, tag_2]
sub_benchmark(benchmark_2, result_2)
sub_site(site_2, result_2)
sub_flavor(flavor_3, result_2)
sub_user(user_1, result_2)
