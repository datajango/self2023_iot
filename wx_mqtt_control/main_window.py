import wx
import paho.mqtt.client as mqtt
import json
from wx_mqtt_control.mqtt_broker_dialog import MQTTBrokerDialog
from wx_mqtt_control.mqtt_broker_manager import BrokerManager

from wx_mqtt_control.mqtt_client_manager import MQTTClientManager
from wx_mqtt_control.device_dialog import DeviceDialog
from wx_mqtt_control.log_dialog import LogDialog
from wx_mqtt_control.publish_dialog import PublishDialog


class MainWindow(wx.Frame):

    def __init__(self, 
                 parent, 
                 title, 
                 config_manager, 
                 broker_manager,
                 logger): 
        super(MainWindow, self).__init__(parent, 
                                         title = title, 
                                         size = (350,300))         
        self.config_manager = config_manager
        self.broker_manager = broker_manager
        self.logger = logger
        
        self.message_counter = 0

        self.InitUI()         

        self.client_manager = MQTTClientManager(self.on_connect, 
                                                self.on_message)
                
        self.broker_dialog = MQTTBrokerDialog(parent, 
                                              broker_manager,
                                              self.on_connect_to_broker,
                                              self.on_disconnect_from_broker)
        self.log_dialog = LogDialog(self)
        #self.pub_dialog = PublishDialog(self)
        #self.devices_dialog = DeviceDialog(self)
        self.log_dialog.Show()        
        self.broker_dialog.Show()
        #self.pub_dialog.Show()
        #self.devices_dialog.Show()

        self.position_windows()


    def position_windows(self):
        # Get screen size
        screen_size = wx.Display().GetGeometry().GetSize()

        # Calculate position for centering the window
        x = (screen_size[0] - 600) // 2
        y = (screen_size[1] - 600) // 2

        # Set position and size
        self.SetPosition((x, y))
        self.SetSize((600, 600))

        # Calculate position        
        main_pos = self.GetPosition()
        x = main_pos[0] - 400
        y = main_pos[1]

        # Set position and size
        self.log_dialog.SetPosition((x, y))
        self.log_dialog.SetSize((400, 600))

        # Calculate position
        main_pos = self.GetPosition()
        main_size = self.GetSize()
        x = main_pos[0] + main_size[0]
        y = main_pos[1]

        # Set position and size
        self.broker_dialog.SetPosition((x, y))
        self.broker_dialog.SetSize((600, 600))


    def InitUI(self): 
        panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.HORIZONTAL) 
        self.text = wx.TextCtrl(panel, style = wx.TE_MULTILINE, size = (300,200)) 
        box.Add(self.text, 1, flag = wx.EXPAND) 
        panel.SetSizer(box) 

        self.create_menu()

    def create_menu(self):
        # Adding a menu bar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        #self.Bind(wx.EVT_MENU, self.OnConnections, connectItem)

        self.menu_bar = wx.MenuBar()
        self.file_menu = wx.Menu()
        
        # Add a Connections menu item
        self.connect_item = self.file_menu.Append(wx.ID_ANY, "Brokers", "Open MQTT Brokers Dialog")
        self.Bind(wx.EVT_MENU, self.on_show_broker_dialog, self.connect_item)

        # Add a Publish menu item
        self.publish_item = self.file_menu.Append(wx.ID_ANY, "Publish")
        self.Bind(wx.EVT_MENU, self.on_show_publish_dialog, self.publish_item)

        # Add a Log menu item
        self.log_item = self.file_menu.Append(wx.ID_ANY, "View Log")
        self.Bind(wx.EVT_MENU, self.on_show_log_dialog, self.log_item)

        # Add a Log menu item
        self.devices_item = self.file_menu.Append(wx.ID_ANY, "View Devices")
        self.Bind(wx.EVT_MENU, self.on_show_devices_dialog, self.devices_item)

        self.menu_bar.Append(self.file_menu, "&File")
        self.SetMenuBar(self.menu_bar)
    
    def on_show_publish_dialog(self, event):
        self.pub_dialog.Show()

    def on_show_log_dialog(self, event):
        self.log_dialog.Show()

    def on_show_devices_dialog(self, event):
        self.devices_dialog.Show()

    def on_show_broker_dialog(self, event):
        self.broker_dialog.Show()        

    def on_connect_to_broker(self, broker):
        self.logger.info('Connecting to broker')
        self.log_dialog.log_message(f"Connecting to broker {broker['name']}")
        
        self.client_manager.connect_to_broker(broker)
    
    def on_disconnect_from_broker(self, event):
        self.logger.info('Disconnecting from broker')
        #self.client_manager.disconnect_from_broker(event.broker)
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
       
        client.subscribe("#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        device_id = msg.topic.split('/')[-1]
        payload = json.loads(msg.payload)

        # if device_id not in self.device_panels:
        #     device_panel = DevicePanel(self, device_id)
        #     self.sizer.Add(device_panel, flag=wx.EXPAND)
        #     self.device_panels[device_id] = device_panel

        #self.device_panels[device_id].update(payload)
        self.Layout()

        self.log_dialog.log_message(f'{msg.topic} {str(payload)}')

    