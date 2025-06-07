import unittest
import json
from jsonschema import Draft202012Validator
import os

class TestExtendedReservationData(unittest.TestCase):
    def setUp(self):
        schema_path = os.path.join(os.path.dirname(__file__), 'reservation_schema.json')
        data_path = os.path.join(os.path.dirname(__file__), 'valid_data.json')

        with open(schema_path, 'r', encoding='utf-8') as schema_file:
            self.schema = json.load(schema_file)

        with open(data_path, 'r', encoding='utf-8') as data_file:
            self.data = json.load(data_file)

        self.validator = Draft202012Validator(self.schema)

    def test_data_validates_against_schema(self):
        errors = sorted(self.validator.iter_errors(self.data), key=lambda e: e.path)
        for error in errors:
            print(f"Validation error at {list(error.path)}: {error.message}")
        self.assertFalse(errors, "Data does not conform to schema")

if __name__ == "__main__":
    unittest.main()
