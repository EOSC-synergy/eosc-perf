from app import app
from app.model.database import db
from app.model.data_types import Uploader, Site, Benchmark, Result, Tag

import code

db.create_all()

uploader1 = Uploader(email='user1@example.com')
uploader2 = Uploader(email='user@example.com')
db.session.add(uploader1)

site1 = Site(short_name='rpi', address='192.168.1.2', description="My cool raspberry pi")
site2 = Site(short_name="terrapc", address='127.0.0.1', description="My strong desktop PC")
db.session.add(site1)
db.session.add(site2)

benchmark1 = Benchmark(docker_name='user/bench:version', uploader=uploader1)
benchmark2 = Benchmark(docker_name='user/otherbench:version', uploader=uploader1)
db.session.add(benchmark1)
db.session.add(benchmark2)

tag1 = Tag(name='neato')
tag2 = Tag(name='cpu')
db.session.add(tag1)
db.session.add(tag2)

uploaders = [uploader1, uploader2]
sites = [site1, site2]
benchmarks = [benchmark1, benchmark2]
tags = [tag1, tag2]

results = []
# massively generate results for resultiterator tests
for uploader in uploaders:
    for site in sites:
        for benchmark in benchmarks:
            for tag in tags:
                result = Result(json="{}", uploader=uploader, site=site, benchmark=benchmark, tags=[tag])
                results.append(result)
                db.session.add(result)

db.session.commit()

code.interact(local=locals())
