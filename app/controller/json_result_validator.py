'''This module provides the service of syntactical 
validation of JSON benchmark results strings'''

import os
import json

DEFAULT_TEMPLATE_PATH = 'config/result_template.json'


class JSONResultValidator:

    def __init__(self, template_path=DEFAULT_TEMPLATE_PATH):
        dirname = os.path.dirname(__file__)
        template_abs_path = os.path.join(dirname, template_path)
        with open(template_abs_path) as template:
            self.template_json = json.load(template)

    def validate_json(self, result_string):
        try:
            result_json = json.loads(result_string)
        except json.JSONDecodeError:
            return False
        return self._has_mandatory_fields(result_json)

    # Check wether the given json has the same keys as the template
    def _has_mandatory_fields(self, result_json):
        return _same_keys(result_json, self.template_json)


def _same_keys(json_one, json_two, check_subkeys=True):
    # Check if both parameters are dictionaries
    if not type(json_one) == type(json_two) == dict:
        return False
    # Check if both dictionaries have the same keys
    if not set(json_one.keys()) == set(json_two.keys()):
        return False
    # Check if both dictionaries have the same subkeys
    keys_with_dict_values = [key for key in json_one.keys() if type(json_one[key]) == dict]
    for key in keys_with_dict_values:
        if not _same_keys(json_one[key], json_two[key]):
            return False
    return True
