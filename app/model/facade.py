""""This module contains the implementation of the Model facade.
Provided are:
  - DatabaseFacade
And as helpers:
  - DatabaseFacade.NotFoundError
  - DatabaseFacade.ToomanyError"""
#from __future__ import annotations
from typing import List
import json
from app.model.data_types import Result, Tag, Benchmark, Uploader, Site, Report, ResultIterator
from .database import db


class DatabaseFacade:
    """Facade class that acts as a middleman between View/Controller and Model classes."""

    class NotFoundError(RuntimeError):
        """Helper exception type to represent queries with no results."""

    class TooManyError(RuntimeError):
        """Helper exception type to represent queries with too many results."""

    def _get_result_iterator(self) -> ResultIterator:
        """Get a result iterator that iterates through every result, unfiltered."""
        return ResultIterator(db.session)

    def _get_result_filterer(self):
        pass

    def _add_uploader(self, email: str) -> bool:
        """Add a new uploader.

        This is a private methods, because uploaders should be added automatically as needed."""
        return self._add_to_db(Uploader(email))

    def get_result(self, uuid: str) -> Result:
        """Fetch a single result by UUID."""
        # prepare query
        results = db.session.query(Result)\
            .filter(Result._uuid == uuid)\
            .all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("result '{}' not found".format(uuid))
        if len(results) > 1:
            # should never happen, UUIDs are famously unique
            raise self.TooManyError("multiple results with same UUID")

        #
        return results[0]

    def get_tag(self, name: str) -> Tag:
        """Fetch a single tag by name."""
        # prepare query
        results = db.session.query(Tag)\
            .filter(Tag._name == name)\
            .all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("tag '{}' not found".format(name))
        if len(results) > 1:
            # should never happen, UUIDs are famously unique
            raise self.TooManyError(
                "multiple tags with same name ({})".format(name))

        #
        return results[0]

    def get_benchmark(self, docker_name: str) -> Benchmark:
        """Fetch a single benchmark by its docker hub name."""
        # prepare query
        results = db.session.query(Benchmark)\
            .filter(Benchmark._docker_name == docker_name)\
            .all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError(
                "benchmark '{}' not found".format(docker_name))
        if len(results) > 1:
            raise self.TooManyError(
                ("multiple benchmarks with same"
                 "docker hub name ({})".format(docker_name)))

        #
        return results[0]

    def get_uploader(self, email: str) -> Uploader:
        """Fetch a single uploader by their email."""
        # prepare query
        results = db.session.query(Uploader)\
            .filter(Uploader._email == email)\
            .all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("uploader '{}' not found".format(email))
        if len(results) > 1:
            raise self.TooManyError(
                "multiple uploaders with same email ({})".format(email))

        #
        return results[0]

    def get_site(self, short_name: str) -> Site:
        """Fetch a single site by its short name."""
        # prepare query
        results = db.session.query(Site)\
            .filter(Site._short_name == short_name)\
            .all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("site '{}' not found".format(short_name))
        if len(results) > 1:
            raise self.TooManyError(
                "multiple sites with same short name ({})".format(short_name))

        #
        return results[0]

    def get_sites(self) -> List[Site]:
        """Get all sites."""
        # prepare query
        results = db.session.query(Site).all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("no sites found")

        #
        return results

    def get_tags(self) -> List[Tag]:
        """Get all tags."""
        # prepare query
        results = db.session.query(Tag).all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("no sites found")

        #
        return results

    def query_results(self, filterJSON: str) -> List[Result]:
        pass

    def query_benchmarks(self, keywords: List[str]) -> List[Benchmark]:
        """Query all benchmarks containing all keywords in the name. Case insensitive."""
        # prepare query
        results = db.session.query(Benchmark)
        # add filter for every keyword
        for keyword in keywords:
            results = results.filter(
                Benchmark._docker_name.ilike('%' + keyword + '%'))

        results = results.all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError(
                "no benchmarks matching the keywords found")

        #
        return results

    def _add_to_db(self, obj: db.Model) -> bool:
        """Add a new model object to the database."""
        try:
            # try adding to session and committing it
            db.session.add(obj)
            db.session.commit()
            return True
        except:
            # reset session to previous state without the object
            db.session.rollback()
            return False

    def _get_or_add_uploader(self, uploader_email: str) -> Uploader:
        """Get a uploader, or add them if they don't exist."""
        uploader = None
        try:
            uploader = self.get_uploader(uploader_email)
        except:
            self._add_uploader(uploader_email)
            uploader = self.get_uploader(uploader_email)
        return uploader

    def add_result(self, content_json: str, metadata_json: str) -> bool:
        """Add new site using site metadata json."""

        # content_json is assumed validated by the Controller
        metadata = None
        try:
            metadata = json.loads(metadata_json)
        except json.JSONDecodeError as decode_error:
            # forward exceptions
            print("illegal result json submitted")
            raise decode_error

        # input validation
        if 'uploader' not in metadata:
            raise ValueError("uploader is missing from result metadata")
        if type(metadata['uploader']) is not str:
            raise TypeError(
                "uploader email must be a string in result metadata")
        if len(metadata['uploader']) < 1:
            raise ValueError("result uploader empty")

        if 'site' not in metadata:
            raise ValueError("site is missing from result metadata")
        if type(metadata['site']) is not str:
            raise TypeError("site must be a string in result metadata")
        if len(metadata['site']) < 1:
            raise ValueError("result site is empty")

        if 'benchmark' not in metadata:
            raise ValueError("benchmark is missing from result metadata")
        if type(metadata['benchmark']) is not str:
            raise TypeError("benchmark must be a string in result metadata")
        if len(metadata['benchmark']) < 1:
            raise ValueError("result benchmark is empty")

        uploader = self._get_or_add_uploader(metadata['uploader'])
        site = None
        try:
            site = self.get_site(metadata['site'])
        except:
            raise ValueError("unknown result site")

        benchmark = None
        try:
            benchmark = self.get_benchmark(metadata['benchmark'])
        except:
            raise ValueError("unknown result benchmark")

        tags = []
        if 'tags' in metadata:
            if type(metadata['tags']) is not list:
                raise TypeError(
                    "tags must be a list of strings in result metadata")
            for tag_name in metadata['tags']:
                if type(tag_name) is not str:
                    raise TypeError(
                        "at least one tag in results metadata is not a string")
                # TODO: fail if tag is unknown, what about auto-adding tags if they do not exist?
                try:
                    tags.append(self.get_tag(tag_name))
                except:
                    raise ValueError("unknown tag")

        result = None
        if len(tags) > 0:
            result = Result(content_json, uploader, site, benchmark, tags=tags)
        else:
            result = Result(content_json, uploader, site, benchmark)

        return self._add_to_db(result)

    def add_site(self, metadata_json: str) -> bool:
        """Add new site using site metadata json."""
        metadata = None
        try:
            metadata = json.loads(metadata_json)
        except json.JSONDecodeError as decode_error:
            # forward exceptions
            print("illegal site json submitted")
            raise decode_error

        # input validation
        if 'short_name' not in metadata:
            raise ValueError("short_name is missing from site metadata")
        if len(metadata['short_name']) < 1:
            raise ValueError("short_name empty")
        if 'address' not in metadata:
            raise ValueError("address is missing from site metadata")
        if len(metadata['address']) < 1:
            raise ValueError("address is empty")

        site = None
        # TODO: description
        if 'name' in metadata and len(metadata['name']) > 0:
            site = Site(metadata['short_name'],
                        metadata['address'], name=metadata['name'])
        else:
            site = Site(metadata['short_name'], metadata['address'])

        return self._add_to_db(site)

    def add_tag(self, name: str) -> bool:
        """Add a new tag."""
        if len(name) < 1:
            raise ValueError("tag name too short")
        return self._add_to_db(Tag(name=name))

    def add_benchmark(self, docker_name: str, uploader_email: str) -> bool:
        """Add a new benchmark."""
        # input validation
        # 3 because: 'user/container' => 'a/b'
        if len(docker_name) < 3:
            raise ValueError("benchmark docker_name impossibly short")
        # 3 because 'user@domain' => 'a@b'
        if len(uploader_email) < 3:
            raise ValueError("benchmark uploader email impossibly short")

        # check if benchmark already exists beforehand to not add new uploader
        # if uploader does not exist
        try:
            self.get_benchmark(docker_name)
            return False
        except:
            pass

        uploader = self._get_or_add_uploader(uploader_email)

        return self._add_to_db(Benchmark(docker_name, uploader))

    def get_report(self, uuid: str) -> Report:
        """Fetch a single report by its UUID."""
        # prepare query
        results = db.session.query(Report)\
            .filter(Report._uuid == uuid)\
            .all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("report '{}' not found".format(uuid))
        if len(results) > 1:
            raise self.TooManyError(
                "multiple reports with same uuid ({})".format(uuid))

        #
        return results[0]

    def get_reports(self, only_unanswered: bool = False) -> List[Report]:
        """Get all or only unanswered reports."""
        # prepare query
        results = db.session.query(Report)

        if only_unanswered:
            results = results.filter(Report._verified == False)

        results = results.all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("no reports found")

        #
        return results


# single global instance
facade = DatabaseFacade()
