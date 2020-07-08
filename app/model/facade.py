from __future__ import annotations 

class DatabaseFacade:
    def __init__(self):
        pass

    def _get_result_iterator(self):
        # this method should stay unimplemented, the signature does not fit the needed constructor args
        pass

    def _get_result_filterer(self):
        pass

    def _add_uploader(self, email: str) -> bool:
        pass

    def get_result(self, uuid: str) -> Result:
        pass

    def get_tag(self, name: str) -> Tag:
        pass

    def get_benchmark(self, docker_name: str) -> Benchmark:
        pass

    def get_uploader(self, email: str) -> Uploader:
        pass

    def get_site(self, short_name: str) -> Site:
        pass

    def get_sites(self) -> List[Site]:
        pass

    def get_tags(self) -> List[Tag]:
        pass

    def query_results(self, filterJSON: str) -> List[Result]:
        pass

    def query_benchmarks(self, keywords: List[str]) -> List[Benchmark]:
        pass

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
