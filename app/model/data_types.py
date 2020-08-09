""""This module contains all data types and associated helpers from the model.
Provided are:
  - Result
  - Uploader
  - Benchmark
  - Tag
  - Site
  - Report
And as helper:
  - ResultIterator"""
from __future__ import annotations
from typing import List
import uuid
from datetime import datetime
from abc import abstractmethod
from sqlalchemy.orm.session import Session
from .database import db


class UUID(db.String):
    """Type alias class to make the design document clearer."""

    def __init__(self):
        db.String.__init__(self, 37)


def new_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


# number of results to fetch from database at once
BATCH_SIZE: int = 100


class ResultIterator:
    """Helper class to handle efficiently fetching a large number of
    benchmark results from the database."""

    def __init__(self, session, **kwargs):
        """Build a new result query iterator.

        Args:
            tags (List[Tag]): The tags the result must be associated to.
            site (Site): The site the result must belong to.
            benchmark (Benchmark): The benchmark the result must belong to.
            uploader (Uploader): The uploader the result must belong to.
        """
        # position within cached results
        self._batch_count: int = 0
        self._batch_offset: int = 0

        # SQLAlchemy session
        self._session = session

        # filter by tags
        self._tags = None
        if 'tags' in kwargs:
            # test if list
            if isinstance(kwargs['tags'], list):
                tags = kwargs['tags']
                if not len(tags) <= 0:
                    # test if list of Tag
                    for tag in tags:
                        if not isinstance(tag, Tag):
                            raise TypeError('"[{}]" is not a Tag'.format(tag))
                self._tags = tags

        # filter by site
        self._site = None
        if 'site' in kwargs:
            if not isinstance(kwargs['site'], Site):
                raise TypeError('"site" is not a Site')
            self._site = kwargs['site']

        # filter by benchmark
        self._benchmark = None
        if 'benchmark' in kwargs:
            if not isinstance(kwargs['benchmark'], Benchmark):
                raise TypeError('"benchmark" is not a Benchmark')
            self._benchmark = kwargs['benchmark']

        # filter by uploader
        self._uploader = None
        if 'uploader' in kwargs:
            if not isinstance(kwargs['uploader'], Uploader):
                raise TypeError('"uploader" is not a Uploader')
            self._uploader = kwargs['uploader']

        self._fetch(self._batch_count)

    def __iter__(self):
        """Generic python iterator function."""
        return self

    def _fetch(self, batch_number: int, batch_size: int = BATCH_SIZE):
        """Load a new batch of cached query results from the database.

        Args:
            batch_number (int): The index of the batch to get.
            batch_size (int): The size of each batch.
        """
        results = self._session.query(Result)

        # build query by filters
        if not self._tags is None:
            # this is the best way I found to do this, should work given not too many tags requested
            # based on: https://stackoverflow.com/a/36975507

            results = results.join(Tag, Result._tags)
            # go through every single tag and check if it is present
            for tag in self._tags:
                results = results.filter(
                    Result._tags.any(Tag._name == tag._name))
        if not self._site is None:
            results = results.filter(Result._site == self._site)
        if not self._benchmark is None:
            results = results.filter(Result._benchmark == self._benchmark)
        if not self._uploader is None:
            results = results.filter(Result._uploader == self._uploader)

        # get batch_number'th batch
        self._cache = results.offset(batch_number * batch_size).limit(batch_size).all()

    def __next__(self):
        """Fetch the next result from cache."""
        # if current batch empty, fetch new batch
        if self._batch_offset == BATCH_SIZE:
            self._batch_count = self._batch_count + 1
            self._fetch(self._batch_count)
            self._batch_offset = 0

        # if arrived at the very end, stop
        if self._batch_offset >= len(self._cache):
            raise StopIteration

        result = self._cache[self._batch_offset]
        self._batch_offset = self._batch_offset + 1
        return result


class Uploader(db.Model):
    """The Uploader class represents an authenticated user that has made usage
    of the system. They may have uploaded benchmarks or benchmark results, or
    added tags or sites."""

    __tablename__ = 'uploader'

    # value columns
    _identifier = db.Column(db.Text, primary_key=True)
    _email = db.Column(db.Text, nullable=False)
    _name = db.Column(db.Text, nullable=False)

    def __init__(self, identifier: str, email: str, name: str):
        """Create a new uploader entry object."""
        super(Uploader, self).__init__(_identifier=identifier, _email=email, _name=name)
    
    def get_id(self) -> str:
        """Get the unique identifier for this uploader."""
        return self._identifier

    def get_email(self) -> str:
        """Get the email address associated with this uploader."""
        return self._email
    
    def get_name(self) -> str:
        """Get a human-readable human name."""
        return self._name

    def get_results(self) -> ResultIterator:
        """Get an iterator for all the results associated with this uploader."""
        return ResultIterator(Session.object_session(self), uploader=self)

    def get_benchmarks(self) -> List[Benchmark]:
        """Get all benchmarks associated with this uploader."""
        return self._benchmarks

    def __repr__(self):
        """Get a human-readable representation string of the uploader."""
        return '<{} {}>'.format(self.__class__.__name__, self._email)


class Benchmark(db.Model):
    """A specific benchmark that was run."""

    __tablename__ = 'benchmark'

    # value columns
    _docker_name = db.Column(db.Text(), nullable=False, primary_key=True)

    # relationship columns
    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'), nullable=False)
    _uploader = db.relationship('Uploader', backref=db.backref('_benchmarks', lazy=True))

    def __init__(self, docker_name: str, uploader: Uploader):
        """Create a new benchmark entry object."""
        super(Benchmark, self).__init__(_docker_name=docker_name, _uploader=uploader)

    def get_docker_name(self) -> str:
        """Get the docker hub identifier of the benchmark, formatted as \"user/image:tagname\"."""
        return self._docker_name

    def get_uploader(self) -> Uploader:
        """Get the user that submitted this benchmark."""
        return self._uploader

    def get_results(self) -> ResultIterator:
        """Get an iterator for all the results associated to this benchmark."""
        return ResultIterator(Session.object_session(self), benchmark=self)

    def __repr__(self):
        """Get a human-readable representation string of the benchmark."""
        return '<{} {}>'.format(self.__class__.__name__, self._docker_name)


class Site(db.Model):
    """The Site class represents a location where a benchmark can be executed."""
    __tablename__ = 'site'

    # value columns
    _short_name = db.Column(db.Text(), primary_key=True, nullable=False)
    _address = db.Column(db.Text(), nullable=False)
    _name = db.Column(db.Text(), nullable=True)
    _description = db.Column(db.Text(), nullable=True)

    def __init__(self, short_name: str, address: str, **kwargs):
        """Create a new site entry object.

        Arg:
            short_name (str): A short identifier for the site.
            address (str): The network address of the site.
            name (str, optional): A human readable name for the site.
            description (str, optional): A human readable description for the site.
        """
        new_args = {}
        if 'name' in kwargs:
            new_args['_name'] = kwargs['name']
        else:
            new_args['_name'] = short_name
        if 'description' in kwargs:
            new_args['_description'] = kwargs['description']

        super(Site, self).__init__(_short_name=short_name, _address=address, **new_args)

    def get_address(self) -> str:
        """Get the network address of the site."""
        return self._address

    def set_address(self, info: str):
        """Update the current network address of the site."""
        self._address = info

    def get_description(self) -> str:
        """Get the human-readable description of the site."""
        return self._description

    def set_description(self, desc: str):
        """Update the current description of the site."""
        self._description = desc

    def get_results(self) -> ResultIterator:
        """Get an iterator for all results associated to this site."""
        return ResultIterator(Session.object_session(self), site=self)

    def get_name(self) -> str:
        """Get the human-readable name of the site."""
        return self._name

    def get_short_name(self) -> str:
        """Get the site's identifier."""
        return self._short_name

    @abstractmethod
    def __repr__(self):
        """Get a human-readable representation string of the site."""
        return '<{} {}>'.format(self.__class__.__name__, self._short_name)


class Tag(db.Model):
    """The Tag class represents a user-created label that can be used for
    filtering a list of results."""
    __tablename__ = 'tag'

    # value columns
    _name = db.Column(db.Text(), primary_key=True)
    _description = db.Column(db.Text(), nullable=True)

    def __init__(self, name: str, **kwargs):
        """Create a new tag entry object.

        Arguments:
        name - Identifier for the tag.
        description (Optional) - Human-readable description for the tag."""
        new_args = {}
        if 'description' in kwargs:
            new_args['_description'] = kwargs['description']

        super(Tag, self).__init__(_name=name, **new_args)

    def get_description(self) -> str:
        """Get the tag's human-readable description."""
        return self._description

    def set_description(self, description: str):
        """Update the current tag's human-readable description."""
        self._description = description

    def get_name(self) -> str:
        """Get the name of the tag."""
        return self._name

    def get_results(self) -> ResultIterator:
        """Get an iterator for all the results associated with this tag."""
        return ResultIterator(Session.object_session(self), tags=[self])

    def __repr__(self):
        """Get a human-readable representation string of the tag."""
        return '<{} {}>'.format(self.__class__.__name__, self._name)


tag_result_association = db.Table(
    'tag_result_association',
    db.Model.metadata,
    db.Column('result_uuid', db.Integer, db.ForeignKey('result._uuid')),
    db.Column('tag_name', db.Integer, db.ForeignKey('tag._name')),
    db.PrimaryKeyConstraint('result_uuid', 'tag_name')
)


class Result(db.Model):
    """The Result class represents a single benchmark result and its contents."""

    __tablename__ = 'result'
    # value columns
    _uuid = db.Column(UUID, primary_key=True, default=new_uuid)
    _json = db.Column(db.Text(), nullable=False)
    _hidden = db.Column(db.Boolean, nullable=False, default=False)

    # relationship columns
    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'), nullable=False)
    _uploader = db.relationship('Uploader', backref=db.backref('_results', lazy=True))

    _site_short_name = db.Column(db.Text, db.ForeignKey('site._short_name'), nullable=False)
    _site = db.relationship('Site', backref=db.backref('_results', lazy=True))

    _benchmark_docker_name = db.Column(db.Text, db.ForeignKey('benchmark._docker_name'),
                                       nullable=False)
    _benchmark = db.relationship('Benchmark', backref=db.backref('_results', lazy=True))

    _tags = db.relationship('Tag', secondary=tag_result_association, backref="_results")

    def __init__(self, json: str, uploader: Uploader, site: Site, benchmark: Benchmark, **kwargs):
        """Create a new result entry object.

        Args:
            json (str): The result's JSON data.
            uploader (Uploader): The user that submitted this result.
            site (Site): The site the benchmark was run on.
            benchmark (Benchmark): The benchmark that was run.
            tags (List[Tag], optional): A list of tags to associated the result with.
        """
        new_args = {}
        if 'tags' in kwargs:
            new_args['_tags'] = kwargs['tags']

        super(Result, self).__init__(_json=json, _uploader=uploader,
                                     _site=site, _benchmark=benchmark, **new_args)

    def get_json(self) -> str:
        """Get the json data of the result."""
        return self._json

    def get_site(self) -> Site:
        """Get the execution site associated with the result."""
        return self._site

    def get_benchmark(self) -> Benchmark:
        """Get the benchmark associated with the result."""
        return self._benchmark

    def get_uploader(self) -> Uploader:
        """Get the uploader associated with the result."""
        return self._uploader

    def get_tags(self) -> List[Tag]:
        """Get all the tags associated with this result."""
        return self._tags

    def set_hidden(self, state: bool):
        """Set the hide state of the result."""
        self._hidden = state

    def get_hidden(self) -> bool:
        """Get the hide state of the result."""
        return self._hidden

    def get_uuid(self) -> str:
        """Get the result's UUID."""
        return self._uuid

    def __repr__(self):
        """Get a human-readable representation string of the result."""
        return '<{} {} ({} {} {} {})>\n'.format(
            self.__class__.__name__, self._uuid,
            self._uploader, self._benchmark, self._site, str(self._tags))


class Report(db.Model):
    """The Report class represents an automated or an user’s report."""

    # value columns
    _uuid = db.Column(UUID, primary_key=True, default=new_uuid)
    _date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    _verified = db.Column(db.Boolean(), nullable=False)
    _verdict = db.Column(db.Boolean(), nullable=False)
    _message = db.Column(db.Text(), nullable=True)
    _type = db.Column(db.String(50))

    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'), nullable=False)
    _uploader = db.relationship('Uploader')

    # enum of report type
    RESULT: int = 1
    BENCHMARK: int = 2
    SITE: int = 3

    __mapper_args__ = {
        'polymorphic_identity': 'report',
        'polymorphic_on': _type
    }

    def __init__(self, **kwargs):
        """Create a new result report entry object."""
        new_args = {}
        # report message
        if 'message' in kwargs:
            new_args['_message'] = kwargs['message']
        # report uploader
        if 'uploader' in kwargs:
            new_args['_uploader'] = kwargs['uploader']
        else:
            raise ValueError("missing uploader in report")
        # specific associations, respective members are added by children
        if self.get_field_name() in kwargs:
            new_args['_' + self.get_field_name()] = kwargs[self.get_field_name()]

        # pass to sqlalchemy constructor
        super(Report, self).__init__(_verified=False, _verdict=False, **new_args)

    def get_date(self) -> datetime.datetime:
        """Get the publication date of the report."""
        return self._date

    def get_message(self) -> str:
        """Get the description message of the report."""
        return self._message

    def get_reporter(self) -> Uploader:
        """Get the user associated with the report that submitted this report."""
        return self._uploader

    def get_status(self) -> str:
        """Get the current status of the report."""
        if not self._verified:
            return 'pending'
        if self._verdict:
            return 'accepted'
        return 'rejected'

    def set_verdict(self, verdict: bool):
        """Update the verdict on the report."""
        self._verdict = verdict
        self._verified = True

    def get_uuid(self) -> str:
        """Get the UUID of this report."""
        return self._uuid

    @abstractmethod
    def get_report_type(self) -> int:
        """Get the enumerated type of the report."""

    @abstractmethod
    def get_field_name(self) -> str:
        """Get the name of the reference field for the constructor."""

    def __repr__(self):
        """Get a human-readable representation string of the report."""
        return '<{} {}>'.format(self.__class__.__name__, self._uuid)


class ResultReport(Report):
    """The ResultReport class represents a report about a benchmark result."""

    __tablename__ = 'result_report'

    _uuid = db.Column(UUID, db.ForeignKey('report._uuid'), primary_key=True)

    # relationship columns
    _result_id = db.Column(db.Text, db.ForeignKey('result._uuid'), nullable=False)
    _result = db.relationship('Result')

    __mapper_args__ = {
        'polymorphic_identity': 'result_report',
    }

    def get_result(self) -> Result:
        """Get the result associated with the report."""
        return self._result

    def get_report_type(self) -> int:
        return Report.RESULT

    def get_field_name(self) -> str:
        return "result"


class BenchmarkReport(Report):
    """The BenchmarkReport class represents a report of a benchmark."""

    __tablename__ = 'benchmark_report'

    _uuid = db.Column(UUID, db.ForeignKey('report._uuid'), primary_key=True)

    # relationship columns
    _benchmark_name = db.Column(db.Text, db.ForeignKey('benchmark._docker_name'), nullable=False)
    _benchmark = db.relationship('Benchmark')

    __mapper_args__ = {
        'polymorphic_identity': 'benchmark_report',
    }

    def get_benchmark(self) -> Benchmark:
        """Get the benchmark associated with the report."""
        return self._benchmark

    def get_report_type(self) -> int:
        return Report.BENCHMARK

    def get_field_name(self) -> str:
        return "benchmark"


class SiteReport(Report):
    """The SiteReport class represents a report of a site."""

    __tablename__ = 'site_report'

    _uuid = db.Column(UUID, db.ForeignKey('report._uuid'), primary_key=True)

    # relationship columns
    _site_name = db.Column(db.Text, db.ForeignKey('site._short_name'), nullable=False)
    _site = db.relationship('Site')

    __mapper_args__ = {
        'polymorphic_identity': 'site_report',
    }

    def get_site(self) -> Site:
        """Get the site associated with the report."""
        return self._site

    def get_report_type(self) -> int:
        return Report.SITE

    def get_field_name(self) -> str:
        return "site"
