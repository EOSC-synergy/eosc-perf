"""This module contains all search filters."""
from abc import abstractmethod
import json
from functools import reduce
from eosc_perf.model.data_types import Result

class Filter:
    """Abstract filter that all concrete Filter implementations inherit from."""
    @abstractmethod
    def filter(self, result: Result) -> bool:
        """Returns whether an element matches the filter or not."""

class BenchmarkFilter(Filter):
    """Filter implementation that matches on Benchmark docker_name."""
    def __init__(self, docker_name: str):
        self.docker_name = docker_name

    def filter(self, result: Result) -> bool:
        """Returns whether the result belongs to the benchmark the filter was primed with."""
        return self.docker_name in result.get_benchmark().get_docker_name()

class UploaderFilter(Filter):
    """Filter implementation that matches on uploader email."""
    def __init__(self, email: str):
        self.email = email

    def filter(self, result: Result) -> bool:
        """Returns whether the result was uploaded by the user the filter was primed with."""
        return result.get_uploader().get_email() == self.email

class SiteFilter(Filter):
    """Filter implementation that matches on site identifier."""
    def __init__(self, site: str):
        self.site = site

    def filter(self, result: Result) -> bool:
        """Returns whether the result was uploaded by the user the filter was primed with."""
        return self.site in result.get_site().get_short_name()

class TagFilter(Filter):
    """Filter implementation that matches on tags."""
    def __init__(self, tag: str):
        self.tag = tag

    def filter(self, result: Result) -> bool:
        """Returns whether the result has the tag the filter was primed with."""
        return self.tag in [t.get_name() for t in result.get_tags()]

class JsonValueFilter(Filter):
    """Filter implementation that matches on a value in the JSON document."""
    def _deep_get(self, dictionary, keys, default=None):
        """Helper to get element based on JSON template"""
        return reduce(lambda d, key: d.get(key, default)
                      if isinstance(d, dict)
                      else default, keys.split("."), dictionary)

    def __init__(self, template: str, value: str, mode: str):
        self.template = template
        self.value = value
        self.mode = mode

    def filter(self, result: Result) -> bool:
        """Returns whether the result has the property the filter was primed with."""
        val = self._deep_get(json.loads(result.get_json()), self.template)
        if val is not None:
            if self.mode == 'equals':
                if isinstance(val, str):
                    return val == self.value
                return abs( float(val) - float(self.value)) < 0.001
            elif self.mode == 'greater_than':
                return float(val) > float(self.value)
            elif self.mode == 'lesser_than':
                return float(val) < float(self.value)
        else:
            return False
