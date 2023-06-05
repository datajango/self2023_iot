class BrokerManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def get_brokers(self):
        return self.config_manager.get_value("connections", [])

    def get_broker(self, name):
        for broker in self.get_brokers():
            if broker["name"] == name:
                return broker
        return None

    def add_or_update_broker(self, name, host, port, username=None, password=None, use_ssl=False):
        broker = self.get_broker(name)
        connections = self.get_brokers()
        if broker is not None:
            # If broker exists, update it
            broker["host"] = host
            broker["port"] = port
            broker["username"] = username
            broker["password"] = password
            broker["use_ssl"] = use_ssl
        else:
            # If broker does not exist, add it
            connections.append({
                "name": name,
                "host": host,
                "port": port,
                "username": username,
                "password": password,
                "use_ssl": use_ssl,
                "topics": []
            })
        # Save configuration
        self.config_manager.save_config()
