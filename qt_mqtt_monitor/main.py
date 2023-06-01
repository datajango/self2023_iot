import json
import logging
from datetime import datetime
from PySide6 import QtCore, QtGui, QtWidgets
from qt_mqtt_monitor.connection_dialog import ConnectionDialog
import paho.mqtt.client as mqtt
from qt_mqtt_monitor.mqtt_client import MqttClient
from qt_mqtt_monitor.config_manager import ConfigurationManager
from logger import setup_logger

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, title="", config_manager=None, logger=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle(title)
        self.config_manager = config_manager
        self.logger = logger
        self.message_counter = 0
        self.setup_mqtt_client()
        self.InitUI()
        self.center()

    def setup_mqtt_client(self):
        default_connection_name = self.config_manager.get_value("default_connection")
        connections = self.config_manager.get_value("connections", [])
        for i, connection in enumerate(connections):
            if connection.get("name") == default_connection_name:
                broker_address = self.config_manager.get_value(f"connections/{i}/broker_address")
                broker_port = self.config_manager.get_value(f"connections/{i}/broker_port", "1883")
                topics = self.config_manager.get_value(f"connections/{i}/topics", [])

                # Create the MQTT Client
                self.mqtt_client = MqttClient(broker_address,
                                              broker_port,
                                              self.on_mqtt_message,
                                              self.on_mqtt_connect)
                if self.config_manager.get_value("auto_connect", False):
                    self.mqtt_client.connect()

                break

    def InitUI(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        box = QtWidgets.QHBoxLayout(central_widget)
        self.text = QtWidgets.QTextEdit()
        box.addWidget(self.text)

        self.create_menu()

    def center(self):
        available_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.setGeometry(available_geometry.width() / 4, available_geometry.height() / 4,
                         available_geometry.width() / 2, available_geometry.height() / 2)

    def OnMessage(self, message):
        self.text.append(message)

    def create_menu(self):
        menuBar = QtWidgets.QMenuBar()
        fileMenu = QtWidgets.QMenu("&File")
        connectItem = fileMenu.addAction("Connections", self.OnConnections)
        menuBar.addMenu(fileMenu)
        self.setMenuBar(menuBar)

    def OnConnections(self):
        dlg = ConnectionDialog(self, self.config_manager)
        dlg.exec()
        dlg.destroy()

    def on_mqtt_message(self, client, userdata, message):
        self.message_counter += 1
        current_time = datetime.now().strftime("%H:%M:%S")

        topic = message.topic
        payload = message.payload.decode("utf-8")
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in configuration file: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error while loading configuration: {str(e)}")

        pretty_data = json.dumps(data, indent=4)

        message = f"({self.message_counter}) {topic}\n{pretty_data}"

        self.logger.info(message)

        self.text.append(message)

    def on_mqtt_connect(self, client, _userdata, flags_dict, result):
        print("Connected to MQTT broker.")
        topics = self.config_manager.get_value("connections/0/topics", [])
        for topic in topics:
            self.mqtt_client.add_route(topic)

    def show_message(self, message):
        self.text.append(message)


def main():
    logger = setup_logger("log", "logfile.log")
    config_manager = ConfigurationManager("settings.json")

    app = QtWidgets.QApplication([])
    frame = MainWindow(title="MQTT Monitor", config_manager=config_manager, logger=logger)
    frame.show()

    logger.info("mqtt_monitor created by Anthony Leotta")
    app.exec()


if __name__ == '__main__':
    main()
