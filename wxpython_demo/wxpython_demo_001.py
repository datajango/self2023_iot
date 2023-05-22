import wx
import paho.mqtt.client as mqtt

class Mywin(wx.Frame): 
    def __init__(self, parent, title): 
        super(Mywin, self).__init__(parent, title = title, size = (350,300)) 
        self.InitUI() 
      
    def InitUI(self): 
        panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.HORIZONTAL) 
        self.text = wx.TextCtrl(panel, style = wx.TE_MULTILINE, size = (300,200)) 
        box.Add(self.text, 1, flag = wx.EXPAND) 
        panel.SetSizer(box) 

    def OnMessage(self, message):
        self.text.AppendText(message+'\n')

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe("mqtt/topic")

def on_message(client, userdata, msg):
    wx.CallAfter(userdata.OnMessage, msg.payload.decode())


def main():
    app = wx.App(False)
    frame = Mywin(None, 'MQTT Monitor')
    frame.Show(True)
    client = mqtt.Client(userdata=frame)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    #client.connect("mqtt.eclipse.org", 1883, 60)
    client.loop_start()
    app.MainLoop()


if __name__ == '__main__':
    main()