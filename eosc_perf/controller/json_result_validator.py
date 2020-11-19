"""This module provides the service of syntactical validation of JSON benchmark result strings."""

import os
import json

from eosc_perf.utility.type_aliases import JSON

DEFAULT_TEMPLATE_PATH = 'config/result_template.json'


class JSONResultValidator:
    """Helper class to validate uploaded result json files."""

    def __init__(self, template_path=DEFAULT_TEMPLATE_PATH):
        dirname = os.path.dirname(__file__)
        template_abs_path = os.path.join(dirname, template_path)
        with open(template_abs_path) as template:
            self.template_json = json.load(template)

    def validate_json(self, result_string: JSON) -> bool:
        """Validate a json string.

        Returns:
            bool: True if valid JSON.
        """
        try:
            result_json = json.loads(result_string)
        except json.JSONDecodeError:
            return False
        return self._has_mandatory_fields(result_json)

    # Check whether the given json has the same keys as the template
    def _has_mandatory_fields(self, result_json):
        return _subset_keys(result_json, self.template_json)


def _subset_keys(json_result: JSON, json_template: JSON, check_subkeys: bool = True) -> bool:
    """Check if a result contains the keys from the template.

    Args:
        json_result (JSON): The result to check.
        json_template (JSON): The template to compare against.
        check_subkeys (bool): Whether to check subkeys.
    Return:
        bool: True if result contains all keys of template.
    """
    # Check if both parameters are dictionaries
    if not (isinstance(json_result, dict) and isinstance(json_template, dict)):
        return False
    # Check if both dictionaries have the same keys
    if not set(json_template.keys()).issubset(set(json_result.keys())):
        diff = set(json_template.keys()).difference(set(json_result.keys()))
        raise ValueError("Uploaded Json misses the following (sub-)keys: {}".format(str(diff)))
    if check_subkeys:
        # Check if both dictionaries have the same subkeys
        keys_with_dict_values = [key for key in json_template.keys() if isinstance(json_template[key], dict)]
        for key in keys_with_dict_values:
            if not _subset_keys(json_result[key], json_template[key]):
                return False
    return True
