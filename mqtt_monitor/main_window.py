import json
import logging
from datetime import datetime
import wx
from connection_dialog import ConnectionDialog
import paho.mqtt.client as mqtt
from mqtt_monitor.mqtt_client import MqttClient

class MainWindow(wx.Frame): 
    def __init__(self, parent, title, config_manager, logger): 
        super(MainWindow, self).__init__(parent, title = title, size = (350,300)) 
        self.config_manager = config_manager
        self.logger = logger
        self.message_counter = 0
        self.InitUI()         
        self.setup_mqtt_client()
        
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
        panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.HORIZONTAL) 
        self.text = wx.TextCtrl(panel, style = wx.TE_MULTILINE, size = (300,200)) 
        box.Add(self.text, 1, flag = wx.EXPAND) 
        panel.SetSizer(box) 

        self.create_menu()

    def OnMessage(self, message):
        self.text.AppendText(message+'\n')

    def create_menu(self):
        # Adding a menu bar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        connectItem = fileMenu.Append(wx.ID_ANY, "Connections", "Open Connections Dialog")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnConnections, connectItem)

    def OnConnections(self, event):
        dlg = ConnectionDialog(self, self.config_manager)
        dlg.ShowModal()
        dlg.Destroy()


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

        wx.CallAfter(self.text.AppendText, message+'\n')

    def on_mqtt_connect(self, client, _userdata, flags_dict, result):
        #if rc == 0:
        print("Connected to MQTT broker.")
        topics = self.config_manager.get_value("connections/0/topics", [])
        for topic in topics:
            self.mqtt_client.add_route(topic)
        # else:
        #     print(f"Failed to connect to MQTT broker with result code {str(rc)}")

    def show_message(self, message):
        # This function will run in the main thread
        # Add your code to update the GUI with the incoming message here
        self.text.AppendText(message+'\n')

