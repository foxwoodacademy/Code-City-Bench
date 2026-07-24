import unittest
import json
import os
from dataweaver.core import DataWeaver
from dataweaver.exceptions import ManifestError, ValidationError, TransformationError

class TestDataWeaver(unittest.TestCase):

    def setUp(self):
        # Create a temporary manifest file for testing
        self.test_manifest_path = 'test_manifest.json'
        self.manifest_content = {
            "metadata": {
                "name": "test_manifest",
                "version": "1.0.0",
                "description": "Test manifest"
            },
            "schema": {
                "temp": {
                    "type": "number",
                    "required": True,
                    "min": -50,
                    "max": 50
                },
                "sensor_id": {
                    "type": "string",
                    "required": True
                },
                "is_active": {
                    "type": "boolean",
                    "required": False
                }
            },
            "transformations": [
                {
                    "action": "rename",
                    "from": "temp",
                    "to": "temperature"
                }
            ]
        }
        with open(self.test_manifest_path, 'w') as f:
            json.dump(self.manifest_content, f)

    def tearDown(self):
        # Remove the temporary manifest file
        if os.path.exists(self.test_manifest_path):
            os.remove(self.test_manifest_path)

    def test_successful_processing(self):
        dw = DataWeaver(self.test_manifest_path)
        input_data = {
            "temp": 25.5,
            "sensor_id": "SN-1234",
            "is_active": True
        }
        expected_output = {
            "temperature": 25.5,
            "sensor_id": "SN-1234",
            "is_active": True
        }
        self.assertEqual(dw.process(input_data), expected_output)

    def test_missing_required_field(self):
        dw = DataWeaver(self.test_manifest_path)
        input_data = {
            "sensor_id": "SN-1234"
        }
        with self.assertRaises(ValidationError) as cm:
            dw.process(input_data)
        self.assertIn("Missing required field: 'temp'", str(cm.exception))

    def test_wrong_type(self):
        dw = DataWeaver(self.test_manifest_path)
        input_data = {
            "temp": "not-a-number",
            "sensor_id": "SN-1234"
        }
        with self.assertRaises(ValidationError) as cm:
            dw.process(input_data)
        self.assertIn("must be of type number", str(cm.exception))

    def test_out_of_range_numeric(self):
        dw = DataWeaver(self.test_manifest_path)
        input_data = {
            "temp": 60,
            "sensor_id": "SN-1234"
        }
        with self.assertRaises(ValidationError) as cm:
            dw.process(input_data)
        self.assertIn("is too large", str(cm.exception))

    def test_invalid_manifest_file(self):
        with self.assertRaises(ManifestError):
            DataWeaver("non_existent.json")

    def test_invalid_json_manifest(self):
        bad_json_path = 'bad.json'
        with open(bad_json_path, 'w') as f:
            f.write("{ invalid json ")
        
        try:
            with self.assertRaises(ManifestError):
                DataWeaver(bad_json_path)
        finally:
            os.remove(bad_json_path)

if __name__ == '__main__':
    unittest.main()
