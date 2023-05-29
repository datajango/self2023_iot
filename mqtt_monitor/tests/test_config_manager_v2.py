import pytest
from mqtt_monitor.config_manager import ConfigurationManager

@pytest.fixture
def config_manager():
    manager = ConfigurationManager()
    manager.config = {
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
    return manager

class TestConfigurationManager:
    def test_get_value_existing(self, config_manager):
        assert config_manager.get_value("connections/0/host") == "localhost"

    def test_get_value_nonexistent_with_default(self, config_manager):
        assert config_manager.get_value("connections/0/nonexistent", default="default") == "default"

    def test_get_value_nonexistent_no_default(self, config_manager):
        assert config_manager.get_value("nonexistent") is None

    def test_get_value_nested(self, config_manager):
        assert config_manager.get_value("settings/log_level") == "INFO"

    def test_get_value_date_and_file_path(self, config_manager):
        assert config_manager.get_value("2023/12/01/README.md") == "Readme file content"
