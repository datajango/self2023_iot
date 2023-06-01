import unittest
from mqtt_monitor.forms.form_manager import FormManager
import os
import json

class TestFormManager(unittest.TestCase):
    def setUp(self):
        # This method will be called before each test
        self.form_manager = FormManager()

    def test_get_form_definition_paths(self):
        # Test that get_form_definition_paths returns a list
        self.assertIsInstance(self.form_manager.(), list)

    def test_load_form_definition_not_found(self):
        # Test loading a form definition file that doesn't exist
        form_definition = self.form_manager.load_form_definition('non_existent_file.json')
        self.assertEqual(form_definition, {})

    def test_load_form_definition_invalid_json(self):
        # Test loading a form definition file with invalid JSON
        # We'll need to create this file first
        with open('invalid.json', 'w') as f:
            f.write('not valid json')
        form_definition = self.form_manager.load_form_definition('invalid.json')
        self.assertEqual(form_definition, {})
        os.remove('invalid.json')

    def test_load_form_definition(self):
        # Test loading a valid form definition
        form_definition_content = {"form_fields": []}
        with open('valid.json', 'w') as f:
            json.dump(form_definition_content, f)
        form_definition = self.form_manager.load_form_definition('valid.json')
        self.assertEqual(form_definition, form_definition_content)
        os.remove('valid.json')


    def test_get_value_existing(self):

        try:
            result = self.manager.load_form(self.form01)
        except Exception as e:
            self.fail(f"load_form raised {type(e)} unexpectedly!")
              
        self.assertIsNotNone(result, "Result is None but expected a value")



if __name__ == "__main__":
    unittest.main()
