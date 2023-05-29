import pytest
from mqtt_monitor.config_manager import ConfigurationManager

def test_get_value():
    """
    This test covers a few different cases for the get_value method.

    It tests getting a value that exists in the config dictionary.
    It tests getting a value that does not exist, with a default value provided.
    It tests getting a value that does not exist, with no default value provided.
    It tests getting a nested value.
    When you run your tests using Visual Studio Code's test features, 
    you should see these tests being executed and their results. If 
    any test fails, pytest will provide a detailed error message that 
    shows what the expected and actual values were.

    Remember to replace from config_manager import ConfigurationManager
    with the actual path where your ConfigurationManager class is defined.
    """

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

    # Test getting a value that exists
    assert manager.get_value("connections/0/host") == "localhost"

    # Test getting a value that does not exist
    assert manager.get_value("connections/0/nonexistent", default="default") == "default"

    # Test getting a value with no default provided
    assert manager.get_value("nonexistent") is None

    # Test getting a nested value
    assert manager.get_value("settings/log_level") == "INFO"

    # Test getting a value with a path that looks like a date and a file
    assert manager.get_value("2023/12/01/README.md") == "Readme file content"