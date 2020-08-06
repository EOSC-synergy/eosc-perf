""""This module contains the implementation of the Model facade.
Provided are:
  - DatabaseFacade
And as helpers:
  - DatabaseFacade.NotFoundError
  - DatabaseFacade.ToomanyError"""
from typing import List
import json
from app.model.data_types import Result, Tag, Benchmark, Uploader, Site,\
    ResultIterator, Report, ResultReport, BenchmarkReport, SiteReport
from app.model.result_filterer import ResultFilterer
from app.model.filters import BenchmarkFilter, UploaderFilter, SiteFilter, TagFilter,\
    JsonValueFilter
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

    def query_results(self, filter_json: str) -> List[Result]:
        """Fetch results based on given filters formatted in JSON."""
        filterer = ResultFilterer()
        decoded_filters = json.loads(filter_json)
        filters = decoded_filters['filters']
        for filter_ in filters:
            if filter_['type'] == 'benchmark':
                filterer.add_filter(BenchmarkFilter(filter_['value']))
            elif filter_['type'] == 'uploader':
                filterer.add_filter(UploaderFilter(filter_['value']))
            elif filter_['type'] == 'site':
                filterer.add_filter(SiteFilter(filter_['value']))
            elif filter_['type'] == 'tag':
                filterer.add_filter(TagFilter(filter_['value']))
            elif filter_['type'] == 'json':
                filterer.add_filter(JsonValueFilter(
                    filter_['key'], filter_['value'], filter_['mode']))
        return filterer.filter(ResultIterator(db.session))

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
        except self.self.NotFoundError:
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
        if not isinstance(metadata['uploader'], str):
            raise TypeError(
                "uploader email must be a string in result metadata")
        if len(metadata['uploader']) < 1:
            raise ValueError("result uploader empty")

        if 'site' not in metadata:
            raise ValueError("site is missing from result metadata")
        if not isinstance(metadata['site'], str):
            raise TypeError("site must be a string in result metadata")
        if len(metadata['site']) < 1:
            raise ValueError("result site is empty")

        if 'benchmark' not in metadata:
            raise ValueError("benchmark is missing from result metadata")
        if not isinstance(metadata['benchmark'], str):
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
            if not isinstance(metadata['tags'], list):
                raise TypeError(
                    "tags must be a list of strings in result metadata")
            for tag_name in metadata['tags']:
                if not isinstance(tag_name, str):
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
        description = None
        if 'description' in metadata and len(metadata['description']) > 0:
            description = metadata['description']
        full_name = None
        if 'name' in metadata and len(metadata['name']) > 0:
            full_name = metadata['name']

        site = Site(metadata['short_name'], metadata['address'], description=description,
                    name=full_name)

        return self._add_to_db(site)

    def add_tag(self, name: str) -> bool:
        """Add a new tag."""
        if len(name) < 1:
            raise ValueError("tag name too short")
        return self._add_to_db(Tag(name=name))

    def add_report(self, metadata: str) -> bool:
        """Add a new report."""
        dic = json.loads(metadata)

        # unpack optional message
        message = None
        if 'message' in dic:
            message = dic['message']

        # sanity checks
        if not 'type' in dic:
            raise ValueError("report missing type")
        if not 'value' in dic:
            raise ValueError("report missing value")
        if 'uploader' not in dic:
            raise ValueError("no uploader in report")

        # check if specified report target exists
        if dic['type'] == 'site':
            try:
                site = self.get_site(dic['value'])
            except self.NotFoundError:
                raise ValueError("unknown site for report")
        elif dic['type'] == 'benchmark':
            try:
                benchmark = self.get_benchmark(dic['value'])
            except self.NotFoundError:
                raise ValueError("unknown benchmark for report")
        elif dic['type'] == 'result':
            try:
                result = self.get_result(dic['value'])
            except self.NotFoundError:
                raise ValueError("unknown result for report")

        # can now add report
        uploader = self._get_or_add_uploader(dic['uploader'])
        success = False
        if dic['type'] == 'site':
            success = self._add_to_db(SiteReport(
                uploader=uploader, message=message, site=site))
        elif dic['type'] == 'benchmark':
            success = self._add_to_db(BenchmarkReport(
                uploader=uploader, message=message, benchmark=benchmark))
        elif dic['type'] == 'result':
            success = self._add_to_db(ResultReport(
                uploader=uploader, message=message, result=result))
        return success

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
        except self.NotFoundError:
            pass

        uploader = self._get_or_add_uploader(uploader_email)

        return self._add_to_db(Benchmark(docker_name, uploader))

    def get_report(self, uuid: str) -> Report:
        """Fetch a single report by its UUID."""
        # query for every type of report
        report_classes = [ResultReport, BenchmarkReport, SiteReport]
        results = []
        for class_type in report_classes:
            results = db.session.query(class_type)\
                .filter(class_type._uuid == uuid)\
                .all()
            # quit if we found the report somewhere
            if len(results) != 0:
                break

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
        results = db.session.query(ResultReport)
        if only_unanswered:
            results = results.filter(ResultReport._verified == False)
        results = results.all()

        benchmarks = db.session.query(BenchmarkReport)
        if only_unanswered:
            benchmarks = benchmarks.filter(BenchmarkReport._verified == False)
        benchmarks = benchmarks.all()

        sites = db.session.query(SiteReport)
        if only_unanswered:
            sites = sites.filter(SiteReport._verified == False)
        sites = sites.all()

        reports = results + benchmarks + sites

        # check number of results
        if len(reports) < 1:
            raise self.NotFoundError("no reports found")

        #
        return reports


# single global instance
facade = DatabaseFacade()
