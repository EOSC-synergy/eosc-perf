""""This module contains the implementation of the Model facade."""
from typing import List, Type
import json
from sqlalchemy.exc import SQLAlchemyError
from eosc_perf.model.data_types import Result, Tag, Benchmark, Uploader, Site,\
    ResultIterator, Report, ResultReport, BenchmarkReport, SiteReport
from eosc_perf.model.result_filterer import ResultFilterer
from eosc_perf.model.filters import BenchmarkFilter, UploaderFilter, SiteFilter, TagFilter,\
    JsonValueFilter
from .database import db


class DatabaseFacade:
    """Facade class that acts as a middleman between View/Controller and Model classes."""

    class NotFoundError(RuntimeError):
        """Helper exception type to represent queries with no results."""

    def get_result(self, uuid: str) -> Result:
        """Fetch a single result by UUID.

        Throws DatabaseFacade.NotFoundError if no such result is found.

        Args:
            uuid (str): The UUID of the result to get.
        Returns:
            Result: The desired result.
        """
        # prepare query
        results = db.session.query(Result).filter(Result._uuid == uuid).all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("result '{}' not found".format(uuid))

        #
        return results[0]

    def get_tag(self, name: str) -> Tag:
        """Fetch a single tag by name.

        Throws DatabaseFacade.NotFoundError if no such tag is found.

        Args:
            name (str): The name of the tag to get.
        Returns:
            Tag: The desired tag.
        """
        # prepare query
        results = db.session.query(Tag).filter(Tag._name == name).all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("tag '{}' not found".format(name))

        #
        return results[0]

    def get_benchmark(self, docker_name: str) -> Benchmark:
        """Fetch a single benchmark by its docker hub name.

        Throws DatabaseFacade.NotFoundError if no such benchmark is found.

        Args:
            docker_name (str): The docker name of the benchmark to get.
        Returns:
            Benchmark: The desired benchmark.
        """
        # prepare query
        results = db.session.query(Benchmark).filter(Benchmark._docker_name == docker_name).all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("benchmark '{}' not found".format(docker_name))

        #
        return results[0]

    def get_uploader(self, identifier: str) -> Uploader:
        """Fetch a single uploader by their unique identifier.

        Throws DatabaseFacade.NotFoundError if no such uploader is found.

        Args:
            identifier (str): The identifier of the uploader to get.
        Returns:
            Uploader: The desired uploader.
        """
        # prepare query
        results = db.session.query(Uploader).filter(Uploader._identifier == identifier).all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("uploader '{}' not found".format(identifier))

        #
        return results[0]

    def get_site(self, short_name: str) -> Site:
        """Fetch a single site by its short name.

        Throws DatabaseFacade.NotFoundError if no such site is found.

        Args:
            short_name (str): The short name of the site to get.
        Returns:
            Site: The desired site.
        """
        # prepare query
        results = db.session.query(Site).filter(Site._short_name == short_name).all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("site '{}' not found".format(short_name))

        #
        return results[0]

    def get_sites(self) -> List[Site]:
        """Get all sites.

        Returns:
            List[Site]: A list of all sites in the database.
        """
        # prepare query
        results = db.session.query(Site).all()

        #
        return results

    def get_tags(self) -> List[Tag]:
        """Get all tags.

        Returns:
            List[Tag]: A list of all tags in the database.
        """
        # prepare query
        results = db.session.query(Tag).all()

        #
        return results

    def get_benchmarks(self) -> List[Benchmark]:
        """Get all benchmarks.

        Returns:
            List[Tag]: A list of all benchmarks in the database.
        """
        # prepare query
        results = db.session.query(Benchmark).all()

        #
        return results

    def query_results(self, filter_json: str) -> List[Result]:
        """Fetch results based on given filters formatted in JSON.

        "type": one of "benchmark", "uploader", "site", "tag", "json",
        "value": the value to match,
        if type == "json": "mode": one of "equals", "greater_than", or "lesser_than"

        Args:
            filter_json (str): A JSON string containing all query filters.
        Returns:
            List[Results]: A list containing the 100 first results in the database matching all filters.
        """
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
        """Query all benchmarks containing all keywords in the name.

        Args:
            keywords (List[str]): A list of all keywords that need to be in the benchmark's docker name.
        Returns:
            List[Benchmark]: A list containing all matching benchmarks in the database.
        """
        # prepare query
        results = db.session.query(Benchmark)

        # add filter for every keyword
        for keyword in keywords:
            results = results.filter(Benchmark._docker_name.contains(keyword))

        results = results.all()

        return results

    def _add_to_db(self, obj: Type[db.Model]) -> bool:
        """Add a new model object to the database.

        Args:
            obj (db.Model): A SQLAlchemy-Model-based object to be added.
        Returns:
            bool: True if adding success.
        """
        try:
            # try adding to session and committing it
            db.session.add(obj)
            db.session.commit()
            return True
        except SQLAlchemyError:
            # reset session to previous state without the object
            db.session.rollback()
            return False

    def _remove_from_db(self, obj: Type[db.Model]) -> bool:
        """Remove a model object from the database.

        Args:
            obj (db.Model): A SQLAlchemy-Model-based object to be removed.
        Returns:
            bool: True if removal successful.
        """
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def _has_uploader(self, uploader: str) -> bool:
        """Input validation helper.

        Args:
            uploader (str): The uploader identifier of the uploader to look for.
        Returns:
            bool: True if the uploader was found.
        """
        if not isinstance(uploader, str):
            return False
        if len(uploader) < 1:
            return False
        try:
            self.get_uploader(uploader)
        except self.NotFoundError:
            return False
        return True

    def _has_site(self, site: str) -> bool:
        """Input validation helper.

        Args:
            site (str): The short name of the site to check for.
        Returns:
            bool: True if the site was found.
        """
        if not isinstance(site, str):
            return False
        if len(site) < 1:
            return False
        try:
            self.get_site(site)
        except self.NotFoundError:
            return False
        return True

    def _has_benchmark(self, benchmark: str) -> bool:
        """Input validation helper.

        Args:
            benchmark (str): The docker_name of the benchmark to check for.
        Returns:
            bool: True of the benchmark was found.
        """
        if not isinstance(benchmark, str):
            return False
        if len(benchmark) < 1:
            return False
        try:
            self.get_benchmark(benchmark)
        except self.NotFoundError:
            return False
        return True

    def add_uploader(self, metadata_json: str) -> bool:
        """Add new uploader using uploader metadata json.

        Args:
            metadata_json (str): The metadata about the new uploader.
        Returns:
            bool: True if adding the uploader was successful.
        """
        #
        metadata = json.loads(metadata_json)

        # input validation
        if 'id' not in metadata:
            raise ValueError("id is missing from uploader metadata")
        if len(metadata['id']) < 1:
            raise ValueError("id empty")
        if 'name' not in metadata:
            raise ValueError("name is missing from uploader metadata")
        if len(metadata['name']) < 1:
            raise ValueError("name is empty")
        if 'email' not in metadata:
            raise ValueError("email is missing from uploader metadata")
        if len(metadata['email']) < 1:
            raise ValueError("email is empty")

        uploader = Uploader(metadata['id'], metadata['email'], metadata['name'])

        return self._add_to_db(uploader)

    def add_result(self, content_json: str, metadata_json: str) -> bool:
        """Add new site using site metadata json.

        Args:
            content_json (str): The JSON of the benchmark result data.
            metadata_json (str): The metadata about the new result.
        Returns:
            bool: True if adding successful.
        """
        # content_json is assumed validated by the Controller
        metadata = json.loads(metadata_json)

        # input validation
        if 'uploader' not in metadata:
            raise ValueError("uploader is missing from result metadata")
        if not self._has_uploader(metadata['uploader']):
            raise ValueError("uploader id is invalid")

        if 'site' not in metadata:
            raise ValueError("site is missing from result metadata")
        if not self._has_site(metadata['site']):
            raise ValueError("site id is invalid")

        if 'benchmark' not in metadata:
            raise ValueError("benchmark is missing from result metadata")
        if not self._has_benchmark(metadata['benchmark']):
            raise ValueError("benchmark name is invalid")

        uploader = self.get_uploader(metadata['uploader'])
        site = self.get_site(metadata['site'])
        benchmark = self.get_benchmark(metadata['benchmark'])

        tags = []
        if 'tags' in metadata:
            if not isinstance(metadata['tags'], list):
                raise TypeError("tags must be a list of strings in result metadata")
            for tag_name in metadata['tags']:
                if not isinstance(tag_name, str):
                    raise TypeError("at least one tag in results metadata is not a string")
                try:
                    tags.append(self.get_tag(tag_name))
                except DatabaseFacade.NotFoundError:
                    raise ValueError("unknown tag")

        return self._add_to_db(Result(content_json, uploader, site, benchmark, tags=tags))

    def add_site(self, metadata_json: str) -> bool:
        """Add new site using site metadata json.

        Args:
            metadata_json (str): The metadata about the site to be added.
        Returns:
            bool: True if adding the site was successful.
        """
        #
        metadata = json.loads(metadata_json)

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

    def remove_site(self, short_name: str) -> bool:
        """Remove a site by short name.

        Args:
            short_name (str): The short name of the site to be removed.
        Returns:
            bool: True if removal was successful.
        """
        try:
            site = self.get_site(short_name)
            return self._remove_from_db(site)
        except self.NotFoundError:
            return False

    def add_tag(self, name: str) -> bool:
        """Add a new tag.

        Args:
            name (str): The name of the tag to add.
        Returns:
            bool: True if adding the tag was successful.
        """
        if len(name) < 1:
            raise ValueError("tag name too short")
        return self._add_to_db(Tag(name=name))

    def add_report(self, metadata: str) -> bool:
        """Add a new report.

        Args:
            metadata (str): The metadata of the report to add.
        Returns:
            bool: True if adding the report was successful.
        """
        #
        dictionary = json.loads(metadata)

        # unpack optional message
        message = None
        if 'message' in dictionary:
            message = dictionary['message']

        # sanity checks
        if 'type' not in dictionary:
            raise ValueError("report missing type")
        if 'value' not in dictionary:
            raise ValueError("report missing value")
        if 'uploader' not in dictionary:
            raise ValueError("no uploader in report")

        try:
            uploader = self.get_uploader(dictionary['uploader'])
        except self.NotFoundError:
            raise ValueError("unknown uploader")

        # check if specified report target exists
        success = False
        if dictionary['type'] == 'site':
            try:
                site = self.get_site(dictionary['value'])
            except self.NotFoundError:
                raise ValueError("unknown site for report")
            success = self._add_to_db(SiteReport(uploader=uploader, site=site, message=message))
        elif dictionary['type'] == 'benchmark':
            try:
                benchmark = self.get_benchmark(dictionary['value'])
            except self.NotFoundError:
                raise ValueError("unknown benchmark for report")
            success = self._add_to_db(BenchmarkReport(uploader=uploader, benchmark=benchmark, message=message))
        elif dictionary['type'] == 'result':
            try:
                result = self.get_result(dictionary['value'])
            except self.NotFoundError:
                raise ValueError("unknown result for report")
            success = self._add_to_db(ResultReport(uploader=uploader, result=result, message=message))

        return success

    def add_benchmark(self, docker_name: str, uploader_id: str) -> bool:
        """Add a new benchmark.

        Args:
            docker_name (str): The docker name of the benchmark to add.
            uploader_id (str): The identifier of the uploader that added this benchmark.
        Returns:
            bool: True if adding the benchmark was successful.
        """
        # 'a/b'
        if len(docker_name) < 3:
            raise ValueError("benchmark docker_name illegally short")
        # 3 because 'user@domain' => 'a@b'
        if not self._has_uploader(uploader_id):
            raise ValueError("unknown uploader")

        uploader = self.get_uploader(uploader_id)

        return self._add_to_db(Benchmark(docker_name, uploader))

    def get_report(self, uuid: str) -> Report:
        """Fetch a single report by its UUID.

        Throws DatabaseFacade.NotFoundError if the report was not found.

        Args:
            uuid (str): The UUID of the report to get.
        Returns:
            Report: The desired report.
        """
        # query for every type of report
        report_classes = [ResultReport, BenchmarkReport, SiteReport]
        results = []
        for class_type in report_classes:
            results = db.session.query(class_type).filter(class_type._uuid == uuid).all()
            # quit if we found the report somewhere
            if len(results) != 0:
                break

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("report '{}' not found".format(uuid))

        #
        return results[0]

    def get_reports(self, only_unanswered: bool = False) -> List[Report]:
        """Get all or only unanswered reports.

        Args:
            only_unanswered (bool): True if it should only return reports with no verdict.
        Returns:
            List[Report]: The list containing the desired reports.
        """
        # prepare query
        # pylint: disable=singleton-comparison
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

        #
        return reports


# single global instance
facade = DatabaseFacade()
