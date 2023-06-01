import json
import os
import logging
import platform
import getpass  # for getting username

class ConfigurationManager:
    def __init__(self, file_name=None):
        if file_name is None:
            self.file_name = "settings.json"
        else:
            self.file_name = file_name
        self.config = {"connections": []}  # initialize with default config
        self.load_config()

    def get_config_paths(self):
        config_paths = []

        # Get username and home path
        username = getpass.getuser()
        home_path = os.path.expanduser("~")

        # Check environment variable
        env_path = os.getenv('CONFIG_PATH')
        if env_path:
            config_paths.append(os.path.abspath(env_path))

        # Check current working directory
        config_paths.append(os.path.join(os.getcwd(), self.file_name))

        # Check user's home directory
        config_paths.append(os.path.join(home_path, self.file_name))

        # Check operating system and add common configuration file paths
        os_name = platform.system()
        os_release = platform.release()

        if os_name == 'Windows' and os_release in ['10', '11']:
            config_paths.append(os.path.join(os.getenv('APPDATA'), self.file_name))
        elif os_name == 'Linux':
            os_version = platform.version()
            if 'Ubuntu' in os_version:
                config_paths.append(os.path.join(home_path, '.config', self.file_name))
                config_paths.append('/etc/' + self.file_name)
        elif os_name == 'Darwin':  # macOS
            config_paths.append(os.path.join(home_path, 'Library', 'Application Support', self.file_name))
        else:
            logging.error(f'Unsupported platform: {os_name}')

        return config_paths


    def load_config(self):
        """Load the configuration from the default location"""
        # This function exists after successful load

        paths = self.get_config_paths()
        
        for path in paths:
            try:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        self.config = json.load(f)
                        logging.info(f"Configuration loaded successfully from {path}")
                        return
            except IOError as e:
                logging.error(f"IOError while loading configuration: {str(e)}")
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in configuration file: {str(e)}")
            except Exception as e:
                logging.error(f"Unexpected error while loading configuration: {str(e)}")

        logging.warning(f"Configuration file not found in locations: {paths}, using default configuration.")
        

    def save_config(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_value_v1(self, path, default=None):
        """Returns the value at the specified path in the config dictionary, or a default value."""
        value = self.config
        path_keys = path.split('/')  # split the path into components
        for key in path_keys:
            try:
                value = value[key]
            except KeyError:
                return default
        return value
    
    def get_value_v2(self, path, default=None):
        segments = path.split('/')
        value = self.config

        for segment in segments:
            if isinstance(value, dict):
                value = value.get(segment)
            else:
                # We've encountered a segment that can't be resolved because 
                # the current value is not a dictionary. Return the default.
                return default

        return value if value is not None else default

    def get_value(self, path, default=None):
        segments = path.split('/')
        value = self.config

        for segment in segments:
            if isinstance(value, dict):
                value = value.get(segment, default)
            elif isinstance(value, list):
                try:
                    idx = int(segment)
                    if idx < len(value):
                        value = value[idx]
                    else:
                        return default
                except ValueError:
                    # segment is not an integer, can't index into the list
                    return default
            else:
                # We've encountered a segment that can't be resolved because 
                # the current value is neither a dictionary nor a list. Return the default.
                return default

        return value if value is not None else default



    # def add(self, path, value):
    #     self.config[path].append(value)
    #     self.save_config()

    # def delete(self, path, value):
    #     self.config[path] = [conn for conn in self.config["connections"] if conn["name"] != connection_name]
    #     self.save_config()
