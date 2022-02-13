"""Module with db db_instances specifications for factories"""
from datetime import datetime
from uuid import uuid4

# User specifications
n_users = 2
users = [{} for _ in range(n_users)]

users[0]["sub"] = "sub_0"
users[0]["iss"] = "https://aai-dev.egi.eu/oidc"
users[0]["email"] = "sub_0@email.com"

users[1]["sub"] = "sub_1"
users[1]["iss"] = "https://aai-dev.egi.eu/oidc"
users[1]["email"] = "sub_1@email.com"


# Tags specifications
n_tags = 4
tags = [{"id": uuid4()} for _ in range(n_tags)]

tags[0]["name"] = "tag0"
tags[0]["description"] = "Description tag 0"

tags[1]["name"] = "tag1"
tags[1]["description"] = "Description tag 1"

tags[2]["name"] = "tag2"
tags[2]["description"] = "Description tag 2"

tags[3]["name"] = "tag3"
tags[3]["description"] = "Description tag 3"


# Benchmark specifications
benchmarks = [{"id": uuid4()} for _ in range(5)]

benchmarks[0]["docker_image"] = "b0"
benchmarks[0]["docker_tag"] = "v1.0"
benchmarks[0]["description"] = "Benchmark 0"
benchmarks[0]["json_schema"] = {"properties": {"time": {"type": "integer"}}}
benchmarks[0]["uploader__email"] = users[0]["email"]
benchmarks[0]["status"] = "approved"

benchmarks[1]["docker_image"] = "b1"
benchmarks[1]["docker_tag"] = "v1.0"
benchmarks[1]["description"] = "Benchmark 1"
benchmarks[1]["json_schema"] = {"properties": {"time": {"type": "integer"}}}
benchmarks[1]["uploader__email"] = users[0]["email"]
benchmarks[1]["status"] = "approved"

benchmarks[2]["docker_image"] = "b2"
benchmarks[2]["docker_tag"] = "v1.0"
benchmarks[2]["description"] = "Benchmark 2"
benchmarks[2]["json_schema"] = {"properties": {"time": {"type": "number"}}}
benchmarks[2]["uploader__email"] = users[1]["email"]
benchmarks[2]["status"] = "on_review"

benchmarks[3]["docker_image"] = "x1"
benchmarks[3]["docker_tag"] = "v1.0"
benchmarks[3]["description"] = "Benchmark in review"
benchmarks[3]["json_schema"] = {"properties": {"time": {"type": "number"}}}
benchmarks[3]["uploader__email"] = users[1]["email"]
benchmarks[3]["status"] = "on_review"

benchmarks[4]["docker_image"] = "x2"
benchmarks[4]["docker_tag"] = "v1.0"
benchmarks[4]["description"] = "Benchmark in review"
benchmarks[4]["json_schema"] = {"properties": {"time": {"type": "number"}}}
benchmarks[4]["uploader__email"] = users[1]["email"]
benchmarks[4]["status"] = "on_review"


# Site specifications
sites = [{"id": uuid4()} for _ in range(3)]

sites[0]["name"] = "site0"
sites[0]["address"] = "address0"
sites[0]["description"] = "Text"
sites[0]["uploader__email"] = users[0]["email"]
sites[0]["status"] = "approved"

sites[1]["name"] = "site1"
sites[1]["address"] = "address1"
sites[1]["description"] = "Text"
sites[1]["uploader__email"] = users[0]["email"]
sites[1]["status"] = "approved"

sites[2]["name"] = "site2"
sites[2]["address"] = "address2"
sites[2]["description"] = "Text"
sites[2]["uploader__email"] = users[1]["email"]
sites[2]["status"] = "on_review"


# Flavor specifications
flavors = [{"id": uuid4()} for _ in range(5)]

flavors[0]["name"] = "flavor0"
flavors[0]["description"] = "Flavor0 site0"
flavors[0]["site__id"] = sites[0]["id"]
flavors[0]["uploader__email"] = users[0]["email"]
flavors[0]["status"] = "approved"

flavors[1]["name"] = "flavor1"
flavors[1]["description"] = "Flavor1 site0"
flavors[1]["site__id"] = sites[0]["id"]
flavors[1]["uploader__email"] = users[0]["email"]
flavors[1]["status"] = "approved"

flavors[2]["name"] = "flavor0"
flavors[2]["description"] = "Flavor0 site1"
flavors[2]["site__id"] = sites[1]["id"]
flavors[2]["uploader__email"] = users[0]["email"]
flavors[2]["status"] = "approved"

flavors[3]["name"] = "flavor1"
flavors[3]["description"] = "Flavor1 site1"
flavors[3]["site__id"] = sites[1]["id"]
flavors[3]["uploader__email"] = users[0]["email"]
flavors[3]["status"] = "approved"

flavors[4]["name"] = "flavor2"
flavors[4]["description"] = "Flavor2 site1"
flavors[4]["site__id"] = sites[1]["id"]
flavors[4]["uploader__email"] = users[1]["email"]
flavors[4]["status"] = "on_review"


# Result specifications
results = [{"id": uuid4()} for _ in range(6)]

results[0]["json"] = {"time": 10, "type": "AMD"}
results[0]["tags"] = [tag for tag in tags[0:2]]
results[0]["benchmark__id"] = benchmarks[0]["id"]
results[0]["flavor__id"] = flavors[0]["id"]
results[0]["uploader__email"] = users[0]["email"]
results[0]["upload_datetime"] = datetime(2000, 1, 1)

results[1]["json"] = {"time": 12, "cpu": True}
results[1]["tags"] = [tag for tag in tags[0:4:2]]
results[1]["benchmark__id"] = benchmarks[1]["id"]
results[1]["flavor__id"] = flavors[2]["id"]
results[1]["uploader__email"] = users[0]["email"]
results[1]["upload_datetime"] = datetime(2020, 1, 1)

results[2]["json"] = {"time": 11, "s1": {"t2": 11}}
results[2]["benchmark__id"] = benchmarks[1]["id"]
results[2]["flavor__id"] = flavors[2]["id"]
results[2]["uploader__email"] = users[1]["email"]
results[2]["upload_datetime"] = datetime(2020, 1, 1)

results[3]["json"] = {"time": 11.0, "s1": {"t2": 11.0}}
results[3]["benchmark__id"] = benchmarks[0]["id"]
results[3]["flavor__id"] = flavors[0]["id"]
results[3]["uploader__email"] = users[0]["email"]
results[3]["upload_datetime"] = datetime(2020, 1, 1)
results[3]["claims"] = ["Claim 1", "Claim 2"]

results[4]["json"] = {"time": 2, "s1": {"t2": 2}, "other": 1.0}
results[4]["benchmark__id"] = benchmarks[0]["id"]
results[4]["flavor__id"] = flavors[0]["id"]
results[4]["uploader__email"] = users[0]["email"]
results[4]["upload_datetime"] = datetime(2020, 1, 1)

results[5]["json"] = {"time": -2, "s1": {"t2": -2}, "other": "two"}
results[5]["benchmark__id"] = benchmarks[0]["id"]
results[5]["flavor__id"] = flavors[0]["id"]
results[5]["uploader__email"] = users[0]["email"]
results[5]["upload_datetime"] = datetime(2020, 1, 1)
