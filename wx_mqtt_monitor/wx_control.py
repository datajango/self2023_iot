import wx
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time
import threading


DEVICE_PROPERTIES = ['state', 'brightness', 'color_temperature']


class ClientManager:
    def __init__(self, brokers, on_connect, on_message, retry_count=5):
        self.clients = []
        self.retry_count = retry_count

        for broker in brokers:
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message
            self.clients.append((client, broker))

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        attempts = 0
        while attempts < self.retry_count:
            for client, broker in self.clients:
                try:
                    client.connect(broker, 1883, 60)
                    client.loop_start()
                    print(f"Connected to broker: {broker}")
                    return
                except Exception as e:
                    print(f"Could not connect to broker: {broker}. Error: {str(e)}")
                    time.sleep(1)  # pause before retrying
            attempts += 1
        print("Could not connect to any broker.")

    def stop_all(self):
        for client, broker in self.clients:
            client.loop_stop(force=False)

mqtt_connectios = {
    "RPI4": {
        "host": "192.168.1.22"
    }, 
    "SET": {
        "host": "192.168.1.32"
    }    
}

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

class PublishDialog(wx.Dialog):
    def __init__(self, parent, client):
        super().__init__(parent, title="Publish MQTT Message")

        self.client = client

        self.topic_label = wx.StaticText(self, label="Topic")
        self.topic_text = wx.TextCtrl(self)
        
        self.payload_label = wx.StaticText(self, label="Payload")
        self.payload_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.send_button = wx.Button(self, label="Send")
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)

        self.close_button = wx.Button(self, label="Close")
        self.close_button.Bind(wx.EVT_BUTTON, self.on_close)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.topic_label)
        self.sizer.Add(self.topic_text, flag=wx.EXPAND)
        self.sizer.Add(self.payload_label)
        self.sizer.Add(self.payload_text, flag=wx.EXPAND)
        self.sizer.Add(self.send_button)
        self.sizer.Add(self.close_button)

        self.SetSizer(self.sizer)

    def on_send(self, event):
        topic = self.topic_text.GetValue()
        payload = self.payload_text.GetValue()

        self.client.publish(topic, payload)

    def on_close(self, event):
        self.Close()


class LogDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="MQTT Message Log", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        
        self.log_textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.log_textctrl, 1, flag=wx.EXPAND)

        self.SetSizer(self.sizer)

    def log_message(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_textctrl.AppendText(f'[{timestamp}] {msg}\n')


class DevicePanel(wx.Panel):
    def __init__(self, parent, device_id):
        super().__init__(parent)

        self.device_id = device_id

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.controls = {}

        for prop in DEVICE_PROPERTIES:
            label = wx.StaticText(self, label=prop)
            control = wx.StaticText(self, label="Unknown")
            self.sizer.Add(label)
            self.sizer.Add(control)
            self.controls[prop] = control

        self.SetSizer(self.sizer)

    def update(self, payload):
        for prop in DEVICE_PROPERTIES:
            if prop in payload:
                self.controls[prop].SetLabel(str(payload[prop]))


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='MQTT Device Monitor')

        self.device_panels = {}
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        #self.client.connect("192.168.1.32", 1883, 60)
        #self.client.loop_start()

        #brokers = ["192.168.1.22", "192.168.1.32"]
        #if not connect_to_first_working_broker(self.client, brokers):
        #    print("Could not connect to any broker.")
        #    return
        
        self.client_manager = ClientManager(brokers, self.on_connect, self.on_message)
        

        self.menu_bar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.publish_item = self.file_menu.Append(wx.ID_ANY, "Publish...")
        self.log_item = self.file_menu.Append(wx.ID_ANY, "Log...")
        self.menu_bar.Append(self.file_menu, "&File")
        self.SetMenuBar(self.menu_bar)

        self.Bind(wx.EVT_MENU, self.on_publish, self.publish_item)
        self.Bind(wx.EVT_MENU, self.on_log, self.log_item)

        self.log_dialog = LogDialog(self)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        device_id = msg.topic.split('/')[-1]
        payload = json.loads(msg.payload)

        if device_id not in self.device_panels:
            device_panel = DevicePanel(self, device_id)
            self.sizer.Add(device_panel, flag=wx.EXPAND)
            self.device_panels[device_id] = device_panel

        self.device_panels[device_id].update(payload)
        self.Layout()

        self.log_dialog.log_message(f'{msg.topic} {str(payload)}')

    def on_publish(self, event):
        dlg = PublishDialog(self, self.client)
        dlg.ShowModal()
        dlg.Destroy()

    def on_log(self, event):
        self.log_dialog.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
