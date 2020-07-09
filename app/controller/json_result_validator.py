'''This module provides the service of syntactical 
validation of JSON benchmark results strings'''

import json

class JSONResultValidator:

    def validate_json(self, result_string):
        try:
            result_json = json.loads(result_string)
        except json.JSONDecodeError:
            return False
        return True
