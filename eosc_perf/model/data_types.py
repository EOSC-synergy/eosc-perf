""""This module defines the abstracting model classes for internal data, like benchmark results, user-created tags,
users and everything else.
"""

from __future__ import annotations

import json
from typing import List, Optional, Dict
import uuid
import datetime
from abc import abstractmethod
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session
from .database import db
from ..utility.type_aliases import JSON


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

    _batch_count: int = 0
    _batch_offset: int = 0

    def __init__(self, session, *, tags: Optional[List[Tag]] = None, site: Optional[Site] = None,
                 benchmark: Optional[Benchmark] = None, uploader: Optional[Uploader] = None):
        """Build a new result query iterator.

        Args:
            session (db.Session): SQLAlchemy session.
            tags (Optional[List[Tag]]): Optional: The tags the result must be associated to.
            site (Optional[Site]): Optional: The site the result must belong to.
            benchmark (Optional[Benchmark]): Optional: The benchmark the result must belong to.
            uploader (Optional[Uploader]): Optional: The uploader the result must belong to.
        """
        # SQLAlchemy session
        self._session = session

        # filter by tags
        self._tags = tags
        self._site = site
        self._benchmark = benchmark
        self._uploader = uploader

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
        if self._tags is not None:
            # this is the best way I found to do this, should work given not too many tags requested
            # based on: https://stackoverflow.com/a/36975507

            results = results.join(Tag, Result._tags)
            # go through every single tag and check if it is present
            for tag in self._tags:
                results = results.filter(Result._tags.any(Tag._name == tag._name))
        if self._site is not None:
            results = results.filter(Result._site == self._site)
        if self._benchmark is not None:
            results = results.filter(Result._benchmark == self._benchmark)
        if self._uploader is not None:
            results = results.filter(Result._uploader == self._uploader)

        # get batch_number'th batch
        self._cache = results.offset(batch_number * batch_size).limit(batch_size).all()

    def __next__(self) -> Result:
        """Fetch the next result from cache.

        Returns:
            Result: The next result.
        """
        # if current batch empty, fetch new batch
        if self._batch_offset == BATCH_SIZE:
            self._batch_count = self._batch_count + 1
            self._fetch(self._batch_count)
            self._batch_offset = 0

        # if arrived at the very end (=> still no items left), stop
        if self._batch_offset >= len(self._cache):
            raise StopIteration

        result = self._cache[self._batch_offset]
        self._batch_offset = self._batch_offset + 1
        return result


class Uploader(db.Model):
    """The Uploader class represents an authenticated user that has made usage of the system. They may have uploaded
    benchmarks or benchmark results, or added tags or sites."""

    __tablename__ = 'uploader'

    # value columns
    _identifier = db.Column(db.Text, primary_key=True)
    _email = db.Column(db.Text, nullable=False)
    _name = db.Column(db.Text, nullable=False)

    _benchmarks: db.Column

    def __init__(self, identifier: str, email: str, name: str):
        """Create a new uploader entry object.

        Args:
            identifier (str): The unique identifier for this uploader.
            email (str): The uploader's email address.
            name (str): The uploader's name.
        """
        super(Uploader, self).__init__(_identifier=identifier, _email=email, _name=name)

    def get_id(self) -> str:
        """Get the unique identifier for this uploader.

        Returns:
            str: This uploader's UUID.
        """
        return self._identifier

    def get_email(self) -> str:
        """Get the email address associated with this uploader.

        Returns:
            str: The uploader's email address.
        """
        return self._email

    def set_email(self, email: str):
        """Update the email address associated with the uploader.

        Args:
            email (str): The new email address.
        """
        self._email = email
        db.session.commit()

    def get_name(self) -> str:
        """Get a human-readable human name.

        Returns:
            str: The uploader's name.
        """
        return self._name

    def set_name(self, name: str):
        """Update the human-readable human human name.

        Args:
            name (str): The new name.
        """
        self._name = name
        db.session.commit()

    def get_results(self) -> ResultIterator:
        """Get an iterator for all the results associated with this uploader.

        Returns:
            ResultIterator: A ResultIterator configured for all results of this uploader.
        """

        return ResultIterator(Session.object_session(self), uploader=self)

    def get_benchmarks(self) -> List[Benchmark]:
        """Get all benchmarks associated with this uploader.

        Returns:
            List[Benchmark]: All benchmarks associated with this uploader.
        """
        return self._benchmarks

    def __repr__(self) -> str:
        """Get a human-readable representation string of the uploader.

        Returns:
            str: A human readable representation string.
        """
        return '<{} {}>'.format(self.__class__.__name__, self._email)


class Benchmark(db.Model):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid confusion and misleading comparisons in case
    the benchmark images change their metrics or scoring scale from version to version.
    """

    # name of table in  database
    __tablename__ = 'benchmark'

    # value columns
    _docker_name = db.Column(db.Text(), nullable=False, primary_key=True)

    _hidden = db.Column(db.Boolean, nullable=False, default=True)

    # relationship columns
    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'), nullable=False)
    _uploader = db.relationship('Uploader', backref=db.backref('_benchmarks', lazy=True))

    _description = db.Column(db.Text, nullable=True)

    _template = db.Column(db.Text, nullable=True)

    def __init__(self, docker_name: str, uploader: Uploader, description: Optional[str] = None,
                 template: Optional[JSON] = None):
        """Create a new benchmark entry object.

        Args:
            docker_name (str): The docker name of the new benchmark.
            uploader (Uploader): The uploader that added this benchmark.
            description (Optional[str]): The description for the benchmark.
            template (Optional[JSON]): The template for the benchmark results.
        """
        super(Benchmark, self).__init__(_docker_name=docker_name, _uploader=uploader, _description=description,
                                        _template=template)

    def get_docker_name(self) -> str:
        """Get the docker hub identifier of the benchmark, formatted as \"user/image:tagname\".

        Returns:
            str: The docker name of the benchmark.
        """
        return self._docker_name

    def get_uploader(self) -> Uploader:
        """Get the user that submitted this benchmark.

        Returns:
            Uploader: The uploader that added this benchmark.
        """
        return self._uploader

    def get_results(self) -> ResultIterator:
        """Get an iterator for all the results associated to this benchmark.

        Returns:
            ResultIterator: An iterator over the associated results.
        """
        return ResultIterator(Session.object_session(self), benchmark=self)

    def set_hidden(self, state: bool):
        """Set the hide state of the benchmark.

        Args:
            state (bool): The new hidden state.
        """
        self._hidden = state
        db.session.commit()

    def get_hidden(self) -> bool:
        """Get the hide state of the benchmark.

        Returns:
            bool: True if hidden.
        """
        return self._hidden

    def set_description(self, description: str):
        """Set the description of the benchmark.

        Args:
            description (str): The new description.
        """
        self._description = description
        db.session.commit()

    def get_description(self):
        """Get the benchmark description.
        """
        return self._description

    def set_template(self, template: JSON):
        """Set a new JSON data template for this benchmark.
        Returns:
            template (JSON): The new JSON data template to use.
        """
        self._template = template
        db.session.commit()

    def has_template(self) -> bool:
        """Check if this benchmark has a specific result template.
        Returns:
            bool: True if this benchmark has a unique template.
        """
        return self._template is not None

    def get_template(self) -> JSON:
        """Get the JSON data template for this benchmark.
        Returns:
            JSON: The template for this benchmark.
        """
        return self._template

    def determine_notable_keys(self) -> List[str]:
        """Get a list containing all notable keys in the template.
        Returns:
            List[str]: All notable keys from this benchmarks template, [] if there is no template.
        """
        if not self.has_template():
            return []
        dictionary: Dict = json.loads(self.get_template())

        def folder(key: str, keydict: Dict) -> List[str]:
            if key.startswith('!') and not isinstance(keydict[key], dict):
                return [key[1:]]

            # recurse into other dicts
            if isinstance(keydict[key], dict):
                # handle '!key': {dict} edge/error case
                if key.startswith('!'):
                    print_key = key[1:]
                else:
                    print_key = key

                # prepend print_key + '.' to all deeper detected notable keys to get full path
                return [*map(lambda subkey: print_key + '.' + subkey,
                             sum([folder(k, keydict[key]) for k in keydict[key].keys()], []))]

            return []

        # start recursion
        return sum([*map(lambda k: folder(k, dictionary), dictionary.keys())], [])

    def __repr__(self) -> str:
        """Get a human-readable representation string of the benchmark.

        Returns:
            str: A human-readable representation string of the benchmark.
        """
        return '<{} {}>'.format(self.__class__.__name__, self._docker_name)


class Site(db.Model):
    """The Site class represents a location where a benchmark can be executed.

    This generally refers to the different virtual machine providers.
    """

    __tablename__ = 'site'

    # value columns
    _identifier = db.Column(db.Text(), primary_key=True, nullable=False)
    _address = db.Column(db.Text(), nullable=False)
    _name = db.Column(db.Text(), nullable=True)
    _description = db.Column(db.Text(), nullable=True)
    _hidden = db.Column(db.Boolean, nullable=False, default=True)

    _flavors: List[SiteFlavor]

    def __init__(self, identifier: str, address: str, **kwargs):
        """Create a new site entry object.

        Arg:
            identifier (str): A short identifier for the site.
            address (str): The network address of the site.
            name (str, optional): A human readable name for the site.
            description (str, optional): A human readable description for the site.
        """
        new_args = {}
        # name defaults to identifier if left out
        if 'name' in kwargs and kwargs['name'] is not None:
            new_args['_name'] = kwargs['name']
        else:
            new_args['_name'] = identifier
        if 'description' in kwargs and kwargs['description'] is not None:
            new_args['_description'] = kwargs['description']

        super(Site, self).__init__(_identifier=identifier, _address=address, **new_args)

    def get_address(self) -> str:
        """Get the network address of the site.

        Returns:
            str: The network address of the site.
        """
        return self._address

    def set_address(self, address: str):
        """Update the current network address of the site.

        Args:
            address (str): The new network address of the site.
        """
        self._address = address
        db.session.commit()

    def get_description(self) -> str:
        """Get the human-readable description of the site.

        Returns:
            str: A human-readable description of the site.
        """
        return self._description

    def set_description(self, desc: str):
        """Update the current description of the site.

        Args:
            desc (str): The new description of the site.
        """
        self._description = desc
        db.session.commit()

    def set_name(self, name: str):
        """Update the full name of the site.

        Args:
            name (str): The full name for the site.
        """
        self._name = name
        db.session.commit()

    def add_flavor(self, flavor: SiteFlavor):
        """Add a new flavor to a site.

        Args:
            flavor (SiteFlavor) - The new flavor.
        """
        self._flavors.append(flavor)
        db.session.commit()

    def get_results(self) -> ResultIterator:
        """Get an iterator for all results associated to this site.

        Returns:
            ResultIterator: An iterator over all results associated with the site.
        """
        return ResultIterator(Session.object_session(self), site=self)

    def get_name(self) -> str:
        """Get the human-readable name of the site.

        Returns:
            str: The human-readable name of the site.
        """
        return self._name

    def get_identifier(self) -> str:
        """Get the site's identifier.

        Returns:
            str: The site's identifier.
        """
        return self._identifier

    def set_hidden(self, state: bool):
        """Set the hide state of the site.

        Args:
            state (bool): Set to true if the site should be hidden.
        """
        self._hidden = state
        db.session.commit()

    def get_hidden(self) -> bool:
        """Get the hide state of the site.

        Returns:
            bool: True if the site is hidden.
        """
        return self._hidden

    def get_flavors(self) -> List[SiteFlavor]:
        return self._flavors

    @abstractmethod
    def __repr__(self) -> str:
        """Get a human-readable representation string of the site.

        Returns:
            str: A human-readable representation string of the site.
        """
        return '<{} {}>'.format(self.__class__.__name__, self._identifier)


class SiteFlavor(db.Model):
    """The SiteFlavor class represents a flavor of virtual machines available for usage on a Site.

    Flavours can be pre-existing options filled in by administrators or a custom configuration by the user.
    Custom flavors' names should be set to SiteFlavor.CUSTOM_FLAVOR and can be distinguished from the pre-filled
    flavors with SiteFlavor.is_unique().
    """

    __tablename__: str = 'siteflavor'

    _uuid = db.Column(UUID, primary_key=True, default=new_uuid)
    _name = db.Column(db.Text())
    _site_identifier = db.Column(db.Text, db.ForeignKey('site._identifier'), nullable=False)
    _site = db.relationship('Site', backref=db.backref('_flavors', lazy=True))
    _custom_text = db.Column(db.Text(), nullable=True, default=None)

    CUSTOM_FLAVOR: str = 'CUSTOM_FLAVOR'

    def __init__(self, name: str, site: Site, custom_text: Optional[str] = None):
        """Create a new site flavor.

        Args:
            name (str) - The name of the flavor.
            site (Site) - The site to associate this result to.
            custom_text (Optional[str]) - Some description text to explain what defines this flavor.
        """
        super(SiteFlavor, self).__init__(_name=name, _site=site, _custom_text=custom_text)

    def get_name(self) -> str:
        """Get the name of this virtual machine flavor.

        Returns:
            str - The name of the flavor.
        """
        return self._name

    def get_site(self) -> Site:
        """Get the site this flavor exists on.

        Returns:
            Site - The site the flavor exists on.
        """
        return self._site

    def get_description(self) -> Optional[str]:
        """Get a user description of a custom flavor, if it exists.

        Returns:
            Optional[str] - The user description of the flavor.
        """
        return self._custom_text

    def get_uuid(self) -> str:
        """Get the UUID for a flavor.

        Returns:
            str - The UUID.
        """
        return self._uuid

    def set_name(self, name: str):
        """Set a new name for a site flavor.

        Args:
            name (str) - The new name for the flavor.
        """
        self._name = name
        db.session.commit()

    def set_description(self, description: str):
        """Set a new description for a site flavor.

        Args:
            description (str) - The new description for the flavor.
        """
        self._custom_text = description
        db.session.commit()

    def is_unique(self) -> bool:
        """Check if this flavor is a unique flavor or a custom/user-added flavor.

        Returns:
            bool: True if the flavor is unique, False if it's a custom flavor.
        """
        return self._name != self.CUSTOM_FLAVOR


class Tag(db.Model):
    """The Tag class represents a user-created label that can be used for filtering a list of results.

    These are entirely created by users and may not necessarily be related to any benchmark output data.
    These may be used to indicate if, for example, a benchmark is used to measure CPU or GPU performance, since some
    benchmarks may be used to test both.
    """

    __tablename__ = 'tag'

    # value columns
    _name = db.Column(db.Text(), primary_key=True)
    _description = db.Column(db.Text(), nullable=True)

    def __init__(self, name: str, **kwargs):
        """Create a new tag entry object.

        Args:
            name (str) - Identifier for the tag.
            description (Optional) - Human-readable description for the tag.
        """
        new_args = {}
        if 'description' in kwargs:
            new_args['_description'] = kwargs['description']

        super(Tag, self).__init__(_name=name, **new_args)

    def get_description(self) -> str:
        """Get the tag's human-readable description.

        Returns:
            str: The tag's human-readable description.
        """
        return self._description

    def set_description(self, description: str):
        """Update the current tag's human-readable description.

        Args:
            description (str): The new description for the tag.
        """
        self._description = description
        db.session.commit()

    def get_name(self) -> str:
        """Get the name of the tag.

        Returns:
            str: The name of the tag.
        """
        return self._name

    def get_results(self) -> ResultIterator:
        """Get an iterator for all the results associated with this tag.

        Returns:
            ResultIterator: An iterator over all results associated with this tag.
        """
        return ResultIterator(Session.object_session(self), tags=[self])

    def __repr__(self) -> str:
        """Get a human-readable representation string of the tag.

        Returns:
            str: A human-readable representation string of the tag.
        """
        return '<{} {}>'.format(self.__class__.__name__, self._name)


tag_result_association = db.Table(
    'tag_result_association',
    db.Model.metadata,
    db.Column('result_uuid', db.Integer, db.ForeignKey('result._uuid')),
    db.Column('tag_name', db.Integer, db.ForeignKey('tag._name')),
    db.PrimaryKeyConstraint('result_uuid', 'tag_name')
)


class Result(db.Model):
    """The Result class represents a single benchmark result and its contents.

    They carry the JSON data output by the ran benchmarks.
    """

    __tablename__ = 'result'
    # value columns
    _uuid = db.Column(UUID, primary_key=True, default=new_uuid)
    _json = db.Column(db.Text(), nullable=False)
    _hidden = db.Column(db.Boolean, nullable=False, default=False)

    # relationship columns
    _uploader_id = db.Column(db.Text, db.ForeignKey('uploader._email'), nullable=False)
    _uploader = db.relationship('Uploader', backref=db.backref('_results', lazy=True))

    _site_identifier = db.Column(db.Text, db.ForeignKey('site._identifier'), nullable=False)
    _site = db.relationship('Site', backref=db.backref('_results', lazy=True))

    _benchmark_docker_name = db.Column(db.Text, db.ForeignKey('benchmark._docker_name'), nullable=False)
    _benchmark = db.relationship('Benchmark', backref=db.backref('_results', lazy=True))

    _flavor_uuid = db.Column(db.Text, db.ForeignKey('siteflavor._uuid'), nullable=False)
    _flavor = db.relationship('SiteFlavor')

    _tags = db.relationship('Tag', secondary=tag_result_association, backref="_results")

    def __init__(self, json_data: str, uploader: Uploader, site: Site, benchmark: Benchmark, flavor: SiteFlavor, **kwargs):
        """Create a new result entry object.

        Args:
            json (str): The result's JSON data.
            uploader (Uploader): The user that submitted this result.
            site (Site): The site the benchmark was run on.
            benchmark (Benchmark): The benchmark that was run.
            flavor (SiteFlavor): The flavor of virtual machine the benchmark was run on.
            tags (List[Tag], optional): A list of tags to associated the result with.
        """
        new_args = {}
        if 'tags' in kwargs and len(kwargs['tags']) > 0:
            new_args['_tags'] = kwargs['tags']

        super(Result, self).__init__(_json=json_data, _uploader=uploader, _site=site, _benchmark=benchmark, _flavor=flavor,
                                     **new_args)

    def get_json(self) -> str:
        """Get the json data of the result.

        Returns:
            str: The benchmark result JSON data.
        """
        return self._json

    def get_site(self) -> Site:
        """Get the execution site associated with the result.

        Returns:
            Site: The site associated with this result.
        """
        return self._site

    def get_benchmark(self) -> Benchmark:
        """Get the benchmark associated with the result.

        Returns:
            Benchmark: The benchmark associated with the result.
        """
        return self._benchmark

    def get_uploader(self) -> Uploader:
        """Get the uploader associated with the result.

        Returns:
            Uploader: The uploader associated with the result.
        """
        return self._uploader

    def get_tags(self) -> List[Tag]:
        """Get all the tags associated with this result.

        Returns:
            List[Tag]: A list of all tags associated with this result.
        """
        return self._tags

    def get_flavor(self) -> SiteFlavor:
        """Get the flavor of virtual machine the benchmark was run on.

        Returns:
            SiteFlavor: The flavor this specific benchmark result resulted from.
        """
        return self._flavor

    def set_hidden(self, state: bool):
        """Set the hide state of the result.

        Args:
            state (bool): True if the result should be hidden.
        """
        self._hidden = state
        db.session.commit()

    def get_hidden(self) -> bool:
        """Get the hide state of the result.

        Returns:
            bool: True if the result is hidden.
        """
        return self._hidden

    def get_uuid(self) -> str:
        """Get the result's UUID.

        Returns:
            str: The UUID of the result.
        """
        return self._uuid

    def add_tag(self, tag: Tag) -> bool:
        """Add a new tag to the result.

        Args:
            tag (Tag): A tag to be associated with the result.
        Returns:
            bool: True if adding the tag was successful.
        """
        # do not add tag twice
        if tag in self._tags:
            return False
        self._tags.append(tag)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    def remove_tag(self, tag: Tag) -> bool:
        """Remove a tag from the result.

        Args:
            tag (Tag): A tag to disassociated from the result.
        Returns:
            bool: True if removing the tag from the result was successful.
        """
        # do not remove not-associated tag
        if tag not in self._tags:
            return False
        self._tags.remove(tag)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    def __repr__(self) -> str:
        """Get a human-readable representation string of the result.

        Returns:
            str: A human-readable representation string of the result.
        """
        return '<{} {} ({} {} {} {})>\n'.format(
            self.__class__.__name__, self._uuid,
            self._uploader, self._benchmark, self._site, str(self._tags))


class Report(db.Model):
    """The Report class represents an automated or an user’s report.

    Reports are automated if used to submit new benchmarks or sites, in which case the report will need to be approved
    before the associated site or benchmark becomes visible.
    Reports can also be manually generated if users choose to report a result from their search results if they suspect
    it may be falsified or incorrect.
    """

    # value columns
    _uuid = db.Column(UUID, primary_key=True, default=new_uuid)
    _date = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)
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

    def __init__(self, uploader: Uploader, message: Optional[str] = None, **kwargs):
        """Create a new result report entry object."""
        new_args = {
            '_message': message if message is not None else "No reason submitted",
            '_uploader': uploader
        }
        # specific associations, respective members are added by children
        if self.get_field_name() in kwargs:
            new_args['_' + self.get_field_name()] = kwargs[self.get_field_name()]

        # pass to sqlalchemy constructor
        super(Report, self).__init__(_verified=False, _verdict=False, **new_args)

    def get_date(self) -> datetime.datetime:
        """Get the publication date of the report.

        Returns:
            datetime.datetime: The publication date.
        """
        return self._date

    def get_message(self) -> str:
        """Get the description message of the report.

        Returns:
            str: The report description message.
        """
        return self._message

    def get_reporter(self) -> Uploader:
        """Get the user that submitted this report.

        Returns:
            Uploader: The uploader that submitted this report.
        """
        return self._uploader

    def get_status(self) -> str:
        """Get the current status of the report.

        Returns:
            str: 'accepted', 'pending', or 'rejected'
        """
        if not self._verified:
            return 'pending'
        if self._verdict:
            return 'accepted'
        return 'rejected'

    def set_verdict(self, verdict: bool):
        """Update the verdict on the report.

        Args:
            verdict (bool): The new verdict to set.
        """
        self._verdict = verdict
        self._verified = True
        db.session.commit()

    def get_uuid(self) -> str:
        """Get the UUID of this report.

        Returns:
            str: The UUID of the report.
        """
        return self._uuid

    @abstractmethod
    def get_report_type(self) -> int:
        """Get the enumerated type of the report.

        Returns:
            int: The type of report.
        """

    @abstractmethod
    def get_field_name(self) -> str:
        """Get the key for the dictionary field to read for result reports.

        Returns:
            str: The key for the dictionary field.
        """

    def __repr__(self) -> str:
        """Get a human-readable representation string of the report.

        Returns:
            str: A human-readable representation string of the report.
        """
        return '<{} {}>'.format(self.__class__.__name__, self._uuid)


class ResultReport(Report):
    """The ResultReport class represents a report about a benchmark result.

    These are normally manually generated.
    """

    __tablename__ = 'result_report'

    _uuid = db.Column(UUID, db.ForeignKey('report._uuid'), primary_key=True)

    # relationship columns
    _result_id = db.Column(db.Text, db.ForeignKey('result._uuid'), nullable=False)
    _result = db.relationship('Result')

    __mapper_args__ = {
        'polymorphic_identity': 'result_report',
    }

    def __init__(self, uploader: Uploader, result: Result, message: Optional[str] = None):
        """Create a new report result.
        Args:
            uploader (Uploader): The uploader that submitted this report.
            result (Result): The result to report.
            message (Optional[str]): Optional report reason.
        """
        super(ResultReport, self).__init__(uploader=uploader, result=result, message=message)

    def get_result(self) -> Result:
        """Get the result associated with the report.

        Returns:
            Result: The result associated with the report.
        """
        return self._result

    def get_report_type(self) -> int:
        """Get the enumerated type of report.

        Returns:
            int: The type of report.
        """
        return Report.RESULT

    def get_field_name(self) -> str:
        """Get the key for the dictionary field to read for result reports.

        Returns:
            str: The key for the dictionary field.
        """
        return "result"


class BenchmarkReport(Report):
    """The BenchmarkReport class represents a report of a benchmark.

    These are automatically generated when a benchmark is submitted.
    """

    __tablename__ = 'benchmark_report'

    _uuid = db.Column(UUID, db.ForeignKey('report._uuid'), primary_key=True)

    # relationship columns
    _benchmark_name = db.Column(db.Text, db.ForeignKey('benchmark._docker_name'), nullable=False)
    _benchmark = db.relationship('Benchmark')

    __mapper_args__ = {
        'polymorphic_identity': 'benchmark_report',
    }

    def __init__(self, uploader: Uploader, benchmark: Benchmark, message: Optional[str] = None):
        """Create a new report result.
        Args:
            uploader (Uploader): The uploader that submitted this report.
            benchmark (Benchmark): The benchmark to report.
            message (Optional[str]): Optional report reason.
        """
        super(BenchmarkReport, self).__init__(uploader=uploader, benchmark=benchmark, message=message)

    def get_benchmark(self) -> Benchmark:
        """Get the benchmark associated with the report."""
        return self._benchmark

    def get_report_type(self) -> int:
        """Get the enumerated type of report.

        Returns:
            int: The type of report.
        """
        return Report.BENCHMARK

    def get_field_name(self) -> str:
        """Get the key for the dictionary field to read for benchmark reports.

        Returns:
            str: The key for the dictionary field.
        """
        return "benchmark"


class SiteReport(Report):
    """The SiteReport class represents a report of a site.

    These are automatically generated when a site is submitted.
    """

    __tablename__ = 'site_report'

    _uuid = db.Column(UUID, db.ForeignKey('report._uuid'), primary_key=True)

    # relationship columns
    _site_name = db.Column(db.Text, db.ForeignKey('site._identifier'), nullable=False)
    _site = db.relationship('Site')

    __mapper_args__ = {
        'polymorphic_identity': 'site_report',
    }

    def __init__(self, uploader: Uploader, site: Site, message: Optional[str] = None):
        """Create a new report result.
        Args:
            uploader (Uploader): The uploader that submitted this report.
            site (Site): The site to report.
            message (Optional[str]): Optional report reason.
        """
        super(SiteReport, self).__init__(uploader=uploader, site=site, message=message)

    def get_site(self) -> Site:
        """Get the site associated with the report.

        Returns:
            Site: The site associated with the report.
        """
        return self._site

    def get_report_type(self) -> int:
        """Get the enumerated type of report.

        Returns:
            int: The type of report.
        """
        return Report.SITE

    def get_field_name(self) -> str:
        """Get the key for the dictionary field to read for site reports.

        Returns:
            str: The key for the dictionary field.
        """
        return "site"
