import paho.mqtt.client as mqtt
import time
import threading

def connect_to_first_working_broker(client, brokers):
    for broker in brokers:
        try:
            client.connect(broker, 1883, 60)
            client.loop_start()
            print(f"Connected to broker: {broker}")
            return True
        except Exception as e:
            print(f"Could not connect to broker: {broker}. Error: {str(e)}")
    return False

def connect_to_brokers(client, brokers, retry_count):
    attempts = 0
    while attempts < retry_count:
        for broker in brokers:
            try:
                client.connect(broker, 1883, 60)
                client.loop_start()
                print(f"Connected to broker: {broker}")
                return True
            except Exception as e:
                print(f"Could not connect to broker: {broker}. Error: {str(e)}")
                attempts += 1
                if attempts >= retry_count:
                    return False
                time.sleep(1)  # pause before retrying
    return False


class MQTTBroker():

    def __init__(self, name, address, port, username, password):
        self.name = name
        self.address = address
        self.port = port
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.name} {self.address} {self.port} {self.username} {self.password}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class MQTTClientManager:
    def __init__(self, on_connect, on_message, retry_count=5):
        self.on_connect = on_connect
        self.on_message = on_message        
        self.retry_count = retry_count

        self.clients = []

    def connect_to_broker(self, broker):
        self.current_broker = broker
        connection_thread = threading.Thread(target=self.try_to_connect, 
                                             args=(broker,),
                                             daemon=True)
        connection_thread.start()        

    def try_to_connect(self, broker):
        # This function will be executed in a new thread
        try:
            # ... insert your connection code here ...
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.on_message = self.on_message

            name = broker['name']
            host = broker['host']
            port = broker['port']

            client.connect(host, int(port), 60)
            client.loop_start()
            print(f"Connected to broker: {name} {host}:{port}")
        except Exception as e:
            print(f"Could not connect to broker: {name} {host}:{port} Error: {str(e)}")

    # def connect(self):
    #     for broker in self.brokers:
    #         client = mqtt.Client()
    #         client.on_connect = self.on_connect
    #         client.on_message = self.on_message
    #         self.clients.append((client, broker))

    #     self.thread = threading.Thread(target=self.run, daemon=True)
    #     self.thread.start()
    
    
    # def run(self):
    #     attempts = 0
    #     while attempts < self.retry_count:
    #         for client, broker in self.clients:
    #             try:
    #                 client.connect(broker, 1883, 60)
    #                 client.loop_start()
    #                 print(f"Connected to broker: {broker}")
    #                 return
    #             except Exception as e:
    #                 print(f"Could not connect to broker: {broker}. Error: {str(e)}")
    #                 time.sleep(1)  # pause before retrying
    #         attempts += 1
    #     print("Could not connect to any broker.")

    # def stop_all(self):
    #     for client, broker in self.clients:
    #         client.loop_stop(force=False)