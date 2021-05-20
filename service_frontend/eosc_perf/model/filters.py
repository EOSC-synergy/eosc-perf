"""The filters module provides a few helper classes used to implement various result search filtering methods, such as
filtering by benchmark names or user tags.
"""
import json
from abc import abstractmethod
from functools import reduce
from typing import Dict, Optional

from eosc_perf.model.data_types import Result


class Filter:
    """Abstract filter that all concrete Filter implementations inherit from."""

    @abstractmethod
    def filter(self, result: Result) -> bool:
        """Returns whether an element matches the filter or not.

        Args:
            result (Result): The result to check the filter for.
        Returns:
            bool: True if the result passes through the filter.
        """


class BenchmarkFilter(Filter):
    """Filter implementation that matches on Benchmark docker_name."""

    def __init__(self, docker_name: str):
        """Create a new filter by benchmark name.

        Args:
            docker_name (str): The docker name of the benchmark to check for.
        """
        self.docker_name = docker_name

    def filter(self, result: Result) -> bool:
        """Returns whether the result belongs to the benchmark the filter was primed with.

        Args:
            result (Result): The result to check the filter for.
        Returns:
            bool: True if the result is from the associated benchmark.
        """
        return self.docker_name in result.benchmark.docker_name


class UploaderFilter(Filter):
    """Filter implementation that matches on uploader email."""

    def __init__(self, email: str):
        """Create a new filter by uploader email address.

        Args:
            email (str): The email of the uploader to check for.
        """
        self.email = email

    def filter(self, result: Result) -> bool:
        """Returns whether the result was uploaded by the user the filter was primed with.

        Args:
            result (Result): The result to check the filter for.
        Returns:
            bool: True if the result was uploaded by the associated uploader.
        """
        return result.uploader.email == self.email


class SiteFilter(Filter):
    """Filter implementation that matches on site identifier."""

    def __init__(self, site: str):
        """Create a new filter by site name.

        Args:
            site (str): The identifier of the site to check for.
        """
        self.site = site

    def filter(self, result: Result) -> bool:
        """Returns whether the result was uploaded by the user the filter was primed with.

        Args:
            result (Result): The result to check the filter for.
        Returns:
            bool: True if the result is from the associated site.
        """
        return self.site in result.site.identifier


class TagFilter(Filter):
    """Filter implementation that matches on tags."""

    def __init__(self, tag: str):
        """Create a new filter by required tag.

        Args:
            tag (str): The name of the tag to check for.
        """
        self.tag = tag

    def filter(self, result: Result) -> bool:
        """Returns whether the result has the tag the filter was primed with.

        Args:
            result (Result): The result to check the filter for.
        Returns:
            bool: True if the result is associated with the associated tag.
        """
        return self.tag in [t.name for t in result.tags]


class JsonValueFilter(Filter):
    """Filter implementation that matches on a value in the JSON document."""

    @staticmethod
    def _deep_get(dictionary: Dict, keys: str, default: Optional[str] = None):
        """Helper to get element based on JSON template.

        Args:
            dictionary (Dict): The dictionary to search the key in.
            keys (str): The nested keys to search.
            default (Optional[str]): An optional default value for the result.
        """
        return reduce(lambda d, key: d.get(key, default)
        if isinstance(d, dict)
        else default, keys.split("."), dictionary)

    def __init__(self, template: str, value: str, mode: str):
        """Create a new filter by JSON sub-value.

        Args:
            template (str): The nested key-sequence to check.
            value (str): The value to compare against.
            mode (str): The comparison mode. May be one of 'equals', 'greater_than', or 'lesser_than'.
        """
        self.template = template
        self.value = value
        self.mode = mode

    def filter(self, result: Result) -> bool:
        """Returns whether the result has the property the filter was primed with.

        Args:
            result (Result): The result to check the filter for.
        Returns:
            bool: True if the result's checked JSON field passes the comparison.
        """
        val = self._deep_get(json.loads(result.json), self.template)
        if val is not None:
            if self.mode == 'equals' and isinstance(val, str):
                return val == self.value
            elif not isinstance(val, str):
                if self.mode == 'equals':
                    return abs(float(val) - float(self.value)) < 0.001
                elif self.mode == 'greater_than':
                    return float(val) > float(self.value)
                elif self.mode == 'lesser_than':
                    return float(val) < float(self.value)
                elif self.mode == 'less_or_equals':
                    return float(val) <= float(self.value)
                elif self.mode == 'greater_or_equals':
                    return float(val) >= float(self.value)
        return False
