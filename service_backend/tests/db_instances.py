"""Module with db db_instances specifications for factories"""
from datetime import datetime
from uuid import uuid4

# User specifications
n_users = 2
users = [{} for _ in range(n_users)]

users[0]['sub'] = "sub_0"
users[0]['iss'] = "egi.com"
users[0]['email'] = "sub_0@email.com"

users[1]['sub'] = "sub_1"
users[1]['iss'] = "egi.com"
users[1]['email'] = "sub_1@email.com"


# Tags specifications
n_tags = 4
tags = [{'id': uuid4()} for _ in range(n_tags)]

tags[0]['name'] = "tag0"
tags[0]['description'] = "Description tag 0"

tags[1]['name'] = "tag1"
tags[1]['description'] = "Description tag 1"

tags[2]['name'] = "tag2"
tags[2]['description'] = "Description tag 2"

tags[3]['name'] = "tag3"
tags[3]['description'] = "Description tag 3"


# Benchmark specifications
benchmarks = [{'id': uuid4()} for _ in range(3)]

benchmarks[0]['docker_image'] = "b0"
benchmarks[0]['docker_tag'] = "v1.0"
benchmarks[0]['description'] = "Benchmark 0"
benchmarks[0]['json_template'] = {'time': ""}
benchmarks[0]['created_by__email'] = users[0]['email']

benchmarks[1]['docker_image'] = "b1"
benchmarks[1]['docker_tag'] = "v1.0"
benchmarks[1]['description'] = "Benchmark 1"
benchmarks[1]['json_template'] = {'time': ""}
benchmarks[1]['created_by__email'] = users[0]['email']

benchmarks[2]['docker_image'] = "b2"
benchmarks[2]['docker_tag'] = "v1.0"
benchmarks[2]['description'] = "Benchmark 2"
benchmarks[2]['json_template'] = {'time': ""}
benchmarks[2]['created_by__email'] = users[0]['email']


# Site specifications
sites = [{'id': uuid4()} for _ in range(2)]

sites[0]['name'] = "site0"
sites[0]['address'] = "address0"
sites[0]['description'] = "Text"
sites[0]['created_by__email'] = users[0]['email']

sites[1]['name'] = "site1"
sites[1]['address'] = "address1"
sites[1]['description'] = "Text"
sites[1]['created_by__email'] = users[0]['email']


# Flavor specifications
flavors = [{'id': uuid4()} for _ in range(4)]

flavors[0]['name'] = "flavor0"
flavors[0]['description'] = "Flavor0 site0"
flavors[0]['site_id'] = sites[0]['id']
flavors[0]['created_by__email'] = users[0]['email']

flavors[1]['name'] = "flavor1"
flavors[1]['description'] = "Flavor1 site0"
flavors[1]['site_id'] = sites[0]['id']
flavors[1]['created_by__email'] = users[0]['email']

flavors[2]['name'] = "flavor0"
flavors[2]['description'] = "Flavor0 site1"
flavors[2]['site_id'] = sites[1]['id']
flavors[2]['created_by__email'] = users[0]['email']

flavors[3]['name'] = "flavor1"
flavors[3]['description'] = "Flavor1 site1"
flavors[3]['site_id'] = sites[1]['id']
flavors[3]['created_by__email'] = users[0]['email']


# Result specifications
results = [{'id': uuid4()} for _ in range(2)]

results[0]['json'] = {'time': 10}
results[0]['tags'] = [tags[0]['name'], tags[1]['name']]
results[0]['benchmark__docker_image'] = benchmarks[0]['docker_image']
results[0]['benchmark__docker_tag'] = benchmarks[0]['docker_tag']
results[0]['site__name'] = sites[0]['name']
results[0]['flavor__name'] = flavors[0]['name']
results[0]['created_by__email'] = users[0]['email']
results[0]['created_at'] = datetime(2000, 1, 1)
results[0]['reports'] = [
	{'message': "Report 1", 'verdict': True},
	{'message': "Report 2", 'verdict': False}
]


results[1] = {'id': uuid4(), 'json': {'time': 12}}
results[1]['tags'] = [tags[0]['name'], tags[2]['name']]
results[1]['benchmark__docker_image'] = benchmarks[1]['docker_image']
results[1]['benchmark__docker_tag'] = benchmarks[1]['docker_tag']
results[1]['site__name'] = sites[1]['name']
results[1]['flavor__name'] = flavors[2]['name']
results[1]['created_by__email'] = users[0]['email']
results[1]['created_at'] = datetime(2020, 1, 1)
results[1]['reports'] = [
	{'message': "Report 1", 'verdict': True},
	{'message': "Report 2", 'verdict': False}
]


