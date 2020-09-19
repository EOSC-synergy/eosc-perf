""""This module contains the result filterer class used by the model.
Provided are:
  - ResultFilterer"""
from typing import List
from app.model.data_types import Result, ResultIterator
from app.model.filters import Filter

class ResultFilterer:
    """Applies a list of filters to a set of results and returns the results that match all
    filters."""
    def __init__(self):
        self._filters = []

    def add_filter(self, filter_: Filter):
        """Adds a filter to the ResultFilterer."""
        self._filters.append(filter_)

    def filter(self, results: ResultIterator) -> List[Result]:
        """Applies all filters to the given list and returns the results that match all of them."""
        filtered = []
        while len(filtered) < 100:
            try:
                result = next(results)
                if all([f.filter(result) for f in self._filters]) and not result.get_hidden():
                    filtered.append(result)
            except StopIteration:
                break
        return filtered
