import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, broker, port, message_callback):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.on_connect = self.on_connect
        self.client.on_message = message_callback

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {str(rc)}")

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def add_route(self, topic, callback=None):
        self.client.subscribe(topic)
        
        if callback:
            self.client.message_callback_add(topic, callback)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
