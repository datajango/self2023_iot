import logging
import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, broker, port, on_message_callback, on_connect_callback=None):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.on_message = on_message_callback
        self.logger = logging.getLogger(__name__)  # Get a logger for this module

        if on_connect_callback:
            self.client.on_connect = on_connect_callback
        else:
            self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            raise Exception(f"Failed to connect with result code: {str(rc)}")
        else:
            print(f"Connected with result code {str(rc)}")

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT broker {self.broker}:{self.port}. Exception:{str(e)}")            

    def add_route(self, topic, callback=None):
        try:
            self.client.subscribe(topic)
        
            if callback:
                self.client.message_callback_add(topic, callback)
        except Exception as e:
            print(f"Failed to add route. Exception: {str(e)}")

    def publish(self, topic, message):
        try:
            self.client.publish(topic, message)
        except Exception as e:
            print(f"Failed to publish message. Exception: {str(e)}")

    def disconnect(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            print(f"Failed to disconnect. Exception: {str(e)}")
