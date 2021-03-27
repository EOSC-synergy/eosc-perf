"""This module provides the service of syntactical validation of JSON benchmark result strings."""

import json
import os
from typing import Optional, Dict

from eosc_perf.utility.type_aliases import JSON

DEFAULT_TEMPLATE_PATH = 'config/result_template.json'


class JSONResultValidator:
    """Helper class to validate uploaded result json files."""

    def __init__(self, template_path=DEFAULT_TEMPLATE_PATH):
        dirname = os.path.dirname(__file__)
        template_abs_path = os.path.join(dirname, template_path)
        with open(template_abs_path) as template:
            self._default_template = json.load(template)

    def validate_json(self, result_data: JSON, template: Optional[JSON] = None, *, skip_keycheck: bool = False) -> bool:
        """Syntactically validate benchmark result JSON and check for key completeness.

        Args:
            result_data (JSON): The benchmark result json to check for validity.
            template (Optional[JSON]): An optional template to check against.
            skip_keycheck (bool): True if the sub-key/template check should be skipped.
        Returns:
            bool: True if syntactically valid and complete JSON.
        """
        try:
            result_json = json.loads(result_data)
        except json.JSONDecodeError:
            return False
        if template is None:
            template = self._default_template
        else:
            template = json.loads(template)
        return skip_keycheck or self._has_mandatory_fields(result_json, template)

    # Check whether the given json has the same keys as the template
    @staticmethod
    def _has_mandatory_fields(result_json: Dict, template: Dict):
        """Check if a given json contains all fields contained in the template.
        Args:
            result_json (Dict): The json data to check for completeness.

        """
        return _subset_keys(result_json, template)


def _remove_prefixes(string: str) -> str:
    """Remove any special prefix characters from the key name.

    These special characters may include:
      - '!': marks interesting keys

    Args:
        string (str): Any key name.
    Returns:
        str: The key name without special prefixes.
    """
    if len(string) >= 2 and string.startswith('!'):
        return string[1:]
    return string


def _subset_keys(json_result: Dict, json_template: Dict, check_sub_keys: bool = True) -> bool:
    """Check if a result contains the keys from the template.

    Args:
        json_result (Dict): The result to check.
        json_template (Dict): The template to compare against.
        check_sub_keys (bool): True if it should recursively check keys.
    Return:
        bool: True if result contains all keys of template.
    """
    # Check if both parameters are dictionaries
    if not (isinstance(json_result, dict) and isinstance(json_template, dict)):
        return False
    # Check if both dictionaries have the same keys
    template_keys_normal_names = [*map(_remove_prefixes, json_template.keys())]
    if not set(template_keys_normal_names).issubset(set(json_result.keys())):
        diff = set(template_keys_normal_names).difference(set(json_result.keys()))
        raise ValueError("Uploaded JSON misses the following (sub-)keys: {}".format(str(diff)))

    if check_sub_keys:
        # Check if both dictionaries have the same subkeys
        keys_with_dict_values = [key for key in json_template.keys() if isinstance(json_template[key], dict)]
        for key in keys_with_dict_values:
            if not _subset_keys(json_result[key], json_template[key]):
                return False
    return True
