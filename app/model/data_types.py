from __future__ import annotations 
from .database import db
import uuid
from datetime import datetime

from typing import List

class UUID(db.String):
    def __init__(self):
        db.String.__init__(self, 37)

def new_uuid() -> str:
    return str(uuid.uuid4())

class ResultIterator:
    pass

class Benchmark(db.Model):
    __tablename__ = 'benchmark'

    # value columns
    _docker_name = db.Column(db.Text(), nullable=False, primary_key=True)

    # relationship columns
    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'),
        nullable=False)
    _uploader = db.relationship('Uploader', backref=db.backref('_benchmarks',
        lazy=True))
    
    def __init__(self, docker_name: str, uploader: Uploader):
        super(Benchmark, self).__init__(_docker_name=docker_name, _uploader=uploader)

    def get_docker_name(self) -> str:
        return self._docker_name
    
    def get_uploader(self) -> Uploader:
        return self._uploader
    
    def get_resuts(self) -> ResultIterator:
        pass

    def __repr__(self):
        return '<Benchmark {}>'.format(self._docker_name)

class Uploader(db.Model):
    """The Uploader class represents an authenticated user that has made usage
    of the system. They may have uploaded benchmarks or benchmark results, or
    added tags or sites."""
    __tablename__ = 'uploader'

    # value columns
    _email = db.Column(db.Text, primary_key=True)

    def __init__(self, email: str):
        super(Uploader, self).__init__(_email=email)

    def get_email(self) -> str:
        return self._email
    
    def get_results(self) -> ResultIterator:
        pass

    def get_benchmarks(self) -> List[Benchmark]:
        return self._benchmarks

    def __repr__(self):
        return '<User {}>'.format(self._email)

class Site(db.Model):
    """The Site class represents a location where a benchmark can be
    executed."""
    __tablename__ = 'site'

    # value columns
    _short_name = db.Column(db.Text(), primary_key=True, nullable=False)
    _address = db.Column(db.Text(), nullable=False)
    _name = db.Column(db.Text(), nullable=True)
    _description = db.Column(db.Text(), nullable=True)

    def __init__(self, short_name: str, address: str, **kwargs):
        new_args = {}
        if 'name' in kwargs:
            new_args['_name'] = kwargs['name']
        else:
            new_args['_name'] = short_name
        if 'description' in kwargs:
            new_args['_description'] = kwargs['description']

        super(Site, self).__init__(_short_name=short_name, _address=address, **new_args)

    def get_address(self) -> str:
        return self._address
    
    def set_address(self, info: str):
        self._address = info
    
    def get_description(self) -> str:
        return self._description
    
    def set_description(self, desc: str):
        self._description = desc
    
    def get_results(self) -> ResultIterator:
        pass

    def get_name(self) -> str:
        return self._name
    
    def get_short_name(self) -> str:
        return self._short_name

    def __repr__(self):
        return '<BenchmarkSite {}>'.format(self._short_name)

class Tag(db.Model):
    """The Tag class represents a user-created label that can be used for
    filtering a list of results."""
    __tablename__ = 'tag'

    # value columns
    _name = db.Column(db.Text(), primary_key=True)
    _description = db.Column(db.Text(), nullable=True)

    def __init__(self, name: str, **kwargs):
        new_args = {}
        if 'description' in kwargs:
            new_args['_description'] = kwargs['description']
        
        super(Tag, self).__init__(_name=name, **new_args)

    def get_description(self) -> str:
        return self._description
    
    def set_description(self, description: str):
        self._description = description
    
    def get_name(self) -> str:
        return self._name
    
    def get_results(self) -> List[Result]:
        return self._results

    def __repr__(self):
        return '<Tag {}>'.format(self._name)

# todo: move elsewhere?
tag_result_association = db.Table('tag_result_association', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('result._uuid')),
    db.Column('right_id', db.Integer, db.ForeignKey('tag._name'))
)

class Result(db.Model):
    """The Result class represents a single benchmark result and its contents."""

    __tablename__ = 'result'
    # value columns
    _uuid = db.Column(UUID, primary_key=True, default=new_uuid)
    _json = db.Column(db.Text(), nullable=False)

    # relationship columns
    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'), nullable=False)
    _uploader = db.relationship('Uploader', backref=db.backref('_results', lazy=True))

    _site_short_name = db.Column(db.Text, db.ForeignKey('site._short_name'), nullable=False)
    _site = db.relationship('Site', backref=db.backref('_results', lazy=True))

    _benchmark_docker_name = db.Column(db.Text, db.ForeignKey('benchmark._docker_name'), nullable=False)
    _benchmark = db.relationship('Benchmark', backref=db.backref('_results', lazy=True))

    _tags = db.relationship('Tag', secondary=tag_result_association, backref="_results")

    def __init__(self, json: str, uploader: Uploader, site: Site, benchmark: Benchmark, **kwargs):
        new_args = {}
        if 'tags' in kwargs:
            new_args['_tags'] = kwargs['tags']
        
        super(Result, self).__init__(_json=json, _uploader=uploader, _site=site, _benchmark=benchmark, **new_args)

    def get_json(self) -> str:
        return self._json
    
    def get_site(self) -> Site:
        return self._site
    
    def get_benchmark(self) -> Benchmark:
        return self._benchmark
    
    def get_uploader(self) -> Uploader:
        return self._uploader
    
    def get_tags(self) -> List[Tag]:
        return self._tags

    def __repr__(self):
        return '<Result {}>'.format(self._uuid)

class Report(db.Model):
    """The Report class represents a user’s report of a benchmark result."""

    # value columns
    _uuid = db.Column(UUID, primary_key=True, default=new_uuid)
    _date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    _verified = db.Column(db.Boolean(), nullable=False)
    _verdict = db.Column(db.Boolean(), nullable=False)
    _message = db.Column(db.Text(), nullable=True)

    # relationship columns
    _result_id = db.Column(db.Text, db.ForeignKey('result._uuid'), nullable=False)
    _result = db.relationship('Result')

    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'), nullable=False)
    _uploader = db.relationship('Uploader')

    def __init__(self, **kwargs):
        new_args = {}
        if 'message' in kwargs:
            new_args['_message'] = kwargs['message']
        super(Report, self).__init__(_verified=False, _veridct=False, **new_args)

    def get_result(self) -> Result:
        return self._result 
    
    def get_date(self) -> datetime.datetime:
        return self._date
    
    def get_message(self) -> str:
        return self._message

    def get_reporter(self) -> Uploader:
        return self._uploader
    
    def get_status(self) -> str:
        if not self._verified:
            return 'pending'
        if self._verdict:
            return 'accepted'
        return 'rejected'
    
    def set_verdict(self, verdict: bool):
        self._verdict = verdict
        self._verified = True
    
    def get_uuid(self) -> str:
        return self._uuid

    def __repr__(self):
        return '<Report {}>'.format(self._uuid)