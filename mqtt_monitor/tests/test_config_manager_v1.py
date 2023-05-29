import unittest
from mqtt_monitor.config_manager import ConfigurationManager

class TestConfigurationManager(unittest.TestCase):
    def setUp(self):
        self.manager = ConfigurationManager()
        self.manager.config = {
            "connections": [
                {"name": "Connection 1", "host": "localhost", "port": 1883},
                {"name": "Connection 2", "host": "example.com", "port": 8883},
            ],
            "settings": {"log_level": "INFO"},
            "2023": {
                "12": {
                    "01": {
                        "README.md": "Readme file content"
                    }
                }
            }
        }

    def test_get_value_existing(self):
        self.assertEqual(self.manager.get_value("connections/0/host"), "localhost")

    def test_get_value_nonexistent_with_default(self):
        self.assertEqual(self.manager.get_value("connections/1/nonexistent", default="default"), "default")

    def test_get_value_nonexistent_no_default(self):
        self.assertIsNone(self.manager.get_value("nonexistent"))

    def test_get_value_nested(self):
        self.assertEqual(self.manager.get_value("settings/log_level"), "INFO")

    def test_get_value_date_and_file_path(self):
        self.assertEqual(self.manager.get_value("2023/12/01/README.md"), "Readme file content")

if __name__ == "__main__":
    unittest.main()
