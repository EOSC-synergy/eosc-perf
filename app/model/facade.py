from __future__ import annotations
from .database import db
from app.model.data_types import Result, Tag, Benchmark, Uploader, Site

class DatabaseFacade:
    def __init__(self):
        pass

    class NotFoundError(RuntimeError):
        """Helper exception type to represent queries with no results."""
        pass

    class TooManyError(RuntimeError):
        """Helper exception type to represent queries with too many results."""
        pass

    def _get_result_iterator(self):
        # this method should stay unimplemented, the signature does not fit the needed constructor args
        pass

    def _get_result_filterer(self):
        pass

    def _add_uploader(self, email: str) -> bool:
        pass

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
            # TODO: test?
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
            # TODO: test?
            raise self.TooManyError("multiple tags with same name ({})".format(name))

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
            raise self.NotFoundError("benchmark '{}' not found".format(docker_name))
        if len(results) > 1:
            # TODO: test?
            raise self.TooManyError("multiple benchmarks with same docker hub name ({})".format(docker_name))

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
            # TODO: test?
            raise self.TooManyError("multiple uploaders with same email ({})".format(email))

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
            # TODO: test?
            raise self.TooManyError("multiple sites with same short name ({})".format(short_name))

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
            results = results.filter(Benchmark._docker_name.ilike('%' + keyword + '%'))
        
        results = results.all()

        # check number of results
        if len(results) < 1:
            raise self.NotFoundError("no benchmarks matching the keywords found")

        #
        return results

    def add_result(self, contentJSON: str, metadataJSON: str) -> bool:
        pass

    def add_site(self, metadataJSON: str) -> bool:
        pass

    def add_tag(self, name: str) -> bool:
        pass

    def add_benchmark(self, docker_name: str, uploader: str) -> bool:
        pass

    def get_report(self, uuid: str) -> Report:
        pass

    def get_reports(self, only_unanswered: bool) -> List[Report]:
        pass
