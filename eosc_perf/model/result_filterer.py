""""This module contains the ResultFilterer class used by the model to filter search results."""
from typing import List

from eosc_perf.model.data_types import Result, ResultIterator
from eosc_perf.model.filters import Filter


class ResultFilterer:
    """The ResultFilterer applies a list of filters to a set of results and returns the results that match all filters.
    This makes use of the helper classes defined in model.filters.
    """

    def __init__(self):
        """Initialize a new ResultFilterer."""
        self._filters = []

    def add_filter(self, new_filter: Filter):
        """Add a filter to the ResultFilterer.

        Args:
            new_filter (Filter): A new filter to apply to the query.
        """
        self._filters.append(new_filter)

    def filter(self, results: ResultIterator) -> List[Result]:
        """Apply all filters to the given list and returns the results that match all of them.

        Args:
            results (ResultIterator): A ResultIterator that supplies benchmark results.
        """
        filtered = []
        while len(filtered) < 100:
            try:
                result = next(results)
                if all([f.filter(result) for f in self._filters]) and not result.get_hidden():
                    filtered.append(result)
            except StopIteration:
                break
        return filtered
