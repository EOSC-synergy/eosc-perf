""""The facade is the interface through which the rest of the application interacts with the model/database. It provides
methods to create, find, and even remove some of the data.
"""
from typing import List, Type, Optional, Tuple
import json

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from eosc_perf.model.data_types import Result, Tag, Benchmark, Uploader, Site, \
    ResultIterator, Report, ResultReport, BenchmarkReport, SiteReport, SiteFlavor
from eosc_perf.model.result_filterer import ResultFilterer
from eosc_perf.model.filters import BenchmarkFilter, UploaderFilter, SiteFilter, TagFilter,\
    JsonValueFilter
from .database import db
from ..utility.type_aliases import JSON


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
        db.session.commit()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("result '{}' not found".format(uuid))

        #
        return results[0]

    def get_site_flavor(self, uuid: str) -> SiteFlavor:
        """Fetch a site flavour by UUID.

        Throws DatabaseFacade.NotFoundError if no such flavour is found.

        Args:
            uuid (str): The UUID of the flavour to get.
        Returns:
            Result: The desired flavour.
        """
        # prepare query
        results = db.session.query(SiteFlavor).filter(SiteFlavor._uuid == uuid).all()
        db.session.commit()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("result '{}' not found".format(uuid))

        #
        return results[0]

    def get_site_flavor_by_name(self, site_name: str, flavor_name: str) -> SiteFlavor:
        """Fetch a site flavour by site and flavor name.

        Throws DatabaseFacade.NotFoundError if no such flavour is found.

        Args:
            site_name (str): The name of the site which has the flavor.
            flavor_name (str): The name of the flavor to find.
        Returns:
            Result: The desired flavour.
        """
        # prepare query
        results = db.session.query(SiteFlavor)\
            .filter(SiteFlavor._site_short_name == site_name)\
            .filter(SiteFlavor._name == flavor_name)\
            .all()
        db.session.commit()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("result '{}' not found".format(flavor_name))

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
        db.session.commit()

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
        db.session.commit()

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
        db.session.commit()

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
        db.session.commit()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("site '{}' not found".format(short_name))

        #
        return results[0]

    @staticmethod
    def get_sites() -> List[Site]:
        """Get all sites.

        Returns:
            List[Site]: A list of all sites in the database.
        """
        # prepare query
        results = db.session.query(Site).all()
        db.session.commit()

        #
        return results

    @staticmethod
    def get_tags() -> List[Tag]:
        """Get all tags.

        Returns:
            List[Tag]: A list of all tags in the database.
        """
        # prepare query
        results = db.session.query(Tag).all()
        db.session.commit()

        #
        return results

    @staticmethod
    def get_benchmarks() -> List[Benchmark]:
        """Get all benchmarks.

        Returns:
            List[Tag]: A list of all benchmarks in the database.
        """
        # prepare query
        results = db.session.query(Benchmark).all()
        db.session.commit()

        #
        return results

    @staticmethod
    def query_results(filter_json: str, disable_uploader_filter: bool = False) -> List[Result]:
        """Fetch results based on given filters formatted in JSON.

        "type": one of "benchmark", "uploader", "site", "tag", "json",
        "value": the value to match,
        if type == "json": "mode": one of "equals", "greater_than", or "lesser_than"

        Args:
            filter_json (str): A JSON string containing all query filters.
            disable_uploader_filter (bool): Whether to *forbid* the upload filter.
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
                # TODO: bit of a hack, detect this in controller?
                if disable_uploader_filter:
                    raise ValueError("unexpected uploader filter")
                filterer.add_filter(UploaderFilter(filter_['value']))
            elif filter_['type'] == 'site':
                filterer.add_filter(SiteFilter(filter_['value']))
            elif filter_['type'] == 'tag':
                filterer.add_filter(TagFilter(filter_['value']))
            elif filter_['type'] == 'json':
                filterer.add_filter(JsonValueFilter(
                    filter_['key'], filter_['value'], filter_['mode']))
        return filterer.filter(ResultIterator(db.session))

    @staticmethod
    def query_benchmarks(keywords: List[str]) -> List[Benchmark]:
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
            results = results.filter(or_(Benchmark._docker_name.contains(keyword), Benchmark._description.contains(keyword)))

        results = results.all()
        db.session.commit()

        return results

    @staticmethod
    def _add_to_db(obj: Type[db.Model]) -> bool:
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

    @staticmethod
    def _remove_from_db(obj: Type[db.Model]) -> bool:
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

    def _has_site_flavor(self, uuid: str) -> bool:
        """Check if a certain site flavor exists.

        Args:
            uuid (str) - The UUID of the site flavor.
        """
        try:
            self.get_site_flavor(uuid)
        except self.NotFoundError:
            return False
        return True

    def add_uploader(self, identifier: str, name: str, email: str) -> bool:
        """Add new uploader using uploader metadata json.

        Args:
            identifier (str): Unique id for this user.
            name (str): Human-readable name for the user.
            email (str): User's email address.
        Returns:
            bool: True if adding the uploader was successful.
        """
        # input validation
        if len(identifier) < 1:
            raise ValueError("id empty")
        if len(name) < 1:
            raise ValueError("name is empty")
        if len(email) < 1:
            raise ValueError("email is empty")

        uploader = Uploader(identifier, email, name)

        success = self._add_to_db(uploader)
        return success

    def add_result(self, content_json: str, uploader_id: str, site_name: str, benchmark_name: str, site_flavor: str,
                   tag_names: List[str] = None) -> bool:
        """Add new site using site metadata json.

        Args:
            content_json (str): The JSON of the benchmark result data.
            uploader_id (str): Identifier for the uploader of this result.
            site_name (str): Short name of the site the benchmark was run on.
            benchmark_name (str): The docker name of the benchmark that was run.
            site_flavor (str): The name of the virtual machine flavor used.
            tag_names (List[str]): Tags to associate to the result.
        Returns:
            bool: True if adding successful.
        """
        if not self._has_uploader(uploader_id):
            raise ValueError("uploader id is invalid")
        if not self._has_site(site_name):
            raise ValueError("site id is invalid")
        if not self._has_benchmark(benchmark_name):
            raise ValueError("benchmark name is invalid")
        if not self._has_site_flavor(site_flavor):
            raise ValueError("site_flavor id " + str(site_flavor) + " is invalid")

        uploader = self.get_uploader(uploader_id)
        site = self.get_site(site_name)
        benchmark = self.get_benchmark(benchmark_name)
        flavor = self.get_site_flavor(site_flavor)

        tags: List[Tag] = []
        if not isinstance(tag_names, list):
            raise TypeError("tags must be in a list")
        if tag_names is not None and len(tag_names) > 0:
            for tag_name in tag_names:
                try:
                    tag = self.get_tag(tag_name)
                    tags.append(tag)
                except self.NotFoundError:
                    raise ValueError("unknown tag " + tag_name)

        return self._add_to_db(Result(content_json, uploader, site, benchmark, flavor=flavor, tags=tags))

    def add_site(self, short_name: str, address: str, *, description: str = None, full_name: str = None) -> bool:
        """Add new site using site metadata json.

        Args:
            short_name (str): Short name for the site. Used as identifier.
            address (str): Network address for the site.
            description (str): Description for the site.
            full_name (str): Human-readable name.
        Returns:
            bool: True if adding the site was successful.
        """

        # input validation
        if len(short_name) < 1:
            raise ValueError("short_name empty")
        if len(address) < 1:
            raise ValueError("address is empty")

        site = Site(short_name, address, description=description, name=full_name)

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
            for flavor in site.get_flavors():
                self._remove_from_db(flavor)
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

    def add_benchmark(self, docker_name: str, uploader_id: str, description: Optional[str] = None,
                      template: Optional[JSON] = None) -> bool:
        """Add a new benchmark.

        Args:
            docker_name (str): The docker name of the benchmark to add.
            uploader_id (str): The identifier of the uploader that added this benchmark.
            description (Optional[str]): The description for the benchmark.
            template (Optional[JSON]): An optional JSON data template to use for the results of this benchmark.
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

        return self._add_to_db(Benchmark(docker_name, uploader, description=description, template=template))

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

    @staticmethod
    def get_reports(only_unanswered: bool = False) -> List[Report]:
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

    def add_flavor(self, name: str, description: str, site_short_name: str) -> Tuple[bool, Optional[str]]:
        if len(name) < 1:
            raise ValueError("flavor name too short")
        try:
            site = self.get_site(site_short_name)
        except self.NotFoundError:
            return False, None
        new_flavor = SiteFlavor(name, site, description if len(description) > 0 else None)
        return self._add_to_db(new_flavor), new_flavor.get_uuid()


# single global instance
facade = DatabaseFacade()
