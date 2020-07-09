from abc import ABC, abstractmethod
import json
from .type_aliases import JSON
from ..model.facade import DatabaseFacade

class AJAXHandler(ABC):
    """Abstract class to represent any AJAX request endpoint."""
    @abstractmethod
    def fetch_data(self, query: JSON) -> JSON:
        """Fetch data corresponding to given query."""
        pass

class SearchAJAXHandler(AJAXHandler):
    """Abstract class to represent a search AJAX request endpoint."""
    def fetch_data(self, query: JSON) -> JSON:
        """Fetch data corresponding to given query."""
        return self.find_results(query)
    
    @abstractmethod
    def find_results(self, query: JSON) -> JSON:
        """Fetch search results corresponding to given query."""
        pass

class ResultSearchAJAX(SearchAJAXHandler):
    """AJAX handler for benchmark result searches with filters."""

    def __init__(self, facade: DatabaseFacade):
        """Set up a new ResultSearchAJAX using the DatabaseFacade."""
        self._facade = facade

    def find_results(self, query: JSON) -> JSON:
        """Fetch benchmark results corresponding to given query."""
        results_dict = { "results": [] }
        results = self._facade.query_results(query)
        for result in results:
            result_dict = {}
            # decode and add to structure to avoid dealing with storing json within jsonj
            result_dict["data"] = json.loads(result.get_json())
            result_dict["site"] = result.get_site().get_short_name()
            result_dict["benchmark"] = result.get_benchmark().get_docker_name()
            result_dict["uploader"] = result.get_uploader().get_email()
            result_dict["tags"] = [tag.get_name() for tag in result.get_tags()]
            results_dict["results"].append(result_dict)
        
        return json.dumps(results_dict)
