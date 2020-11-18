"""This module contains unit tests for the JSONResultValidator class"""

import json
import unittest
from eosc_perf.controller.json_result_validator import JSONResultValidator
from eosc_perf.configuration import configuration

class JSONResultValidatorTest(unittest.TestCase):

    def setUp(self):
        """Called before each test."""
        self.validator = JSONResultValidator()
        configuration.reload()

    def tearDown(self):
        """Called after each test."""
        del self.validator

    def test_empty_json(self):
        js = json.dumps({})
        self.assertRaises(ValueError, self.validator.validate_json, js)

    def test_none(self):
        self.assertRaises(TypeError, self.validator.validate_json, None)

    def test_missing_key(self):
        template = self._load_template()
        js = json.loads(template)
        if len(js.keys()) > 0:
            js.pop(list(js.keys())[0], None)
            self.assertRaises(ValueError, self.validator.validate_json, json.dumps(js))

    def test_missing_subkey(self):
        template = self._load_template()
        js = json.loads(template)
        for key in js.keys():
            if isinstance(js[key], dict):
                if len(js[key].keys()) > 0:
                    js[key].pop(list(js[key].keys())[0], None)
                    self.assertRaises(ValueError, self.validator.validate_json, json.dumps(js))

    def test_wrong_value_type(self):
        template = self._load_template()
        js = json.loads(template)
        for key in js.keys():
            if isinstance(js[key], dict):
                js[key] = [1, 2]
                self.assertFalse(self.validator.validate_json(json.dumps(js)))

    def test_template(self):
        template = self._load_template()
        self.assertTrue(self.validator.validate_json(template))

    def test_template_additional_keys(self):
        template = self._load_template()
        js = json.loads(template)
        for key in js.keys():
            if isinstance(js[key], dict):
                js[key]["new_sub_key"] = 42
        js["new_key"] = "new value"
        js["another_new_key"] = {"new_dict_sub_key": 2}
        self.assertTrue(self.validator.validate_json(json.dumps(js)))

    def _load_template(self):
        with open("eosc_perf/controller/config/result_template.json") as file:
            return file.read()

if __name__ == '__main__':
    unittest.main()
