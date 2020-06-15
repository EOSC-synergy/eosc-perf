from app import app
from app.model.database import db

from app.model.data_types import Uploader, Site, Benchmark, Result, Tag

db.create_all()

uploader1 = Uploader(email='user1@example.com')
db.session.add(uploader1)

site1 = Site(short_name='rpi', address='192.168.1.2', description="My cool raspberry pi")
site2 = Site(short_name="terrapc", address='127.0.0.1', description="My strong desktop PC")
db.session.add(site1)
db.session.add(site2)

benchmark1 = Benchmark(docker_name='user/bench:version', uploader=uploader1)
db.session.add(benchmark1)

tag1 = Tag(name='neato')
tag2 = Tag(name='cpu')

result1 = Result(json="bad", uploader=uploader1, site=site1, benchmark=benchmark1, tags=[tag1, tag2])
result2 = Result(json="good", uploader=uploader1, site=site2, benchmark=benchmark1, tags=[tag2])

db.session.commit()
